#!/usr/bin/env python3
"""Lint composite action and workflow files for two supply-chain pitfalls.

1. Every `uses:` ref must be pinned to a 40-char commit SHA. Tag-only refs
   like `@v4` or `@main` are mutable and can be retargeted upstream.
2. No `${{ inputs.* }}`, `${{ github.event.* }}`, or `${{ github.head_ref }}`
   may appear inside a `run:` body. Those values can contain shell
   metacharacters; route them through env: and reference as quoted bash vars.

Run from the repo root: `python3 .github/scripts/lint_actions.py`.
Exits non-zero if any issue is found, and emits GitHub `::error` annotations
so they show up inline on PRs.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)")
SHA_RE = re.compile(r"@[a-f0-9]{40}(/|$)")
RUN_BLOCK_RE = re.compile(r"^(\s*)run:\s*[|>][-+]?\s*(?:#.*)?$")
RUN_INLINE_RE = re.compile(r"^(\s*)run:\s*(.+)$")
FORBIDDEN_IN_RUN = re.compile(
    r"\$\{\{\s*("
    r"inputs\.[a-zA-Z0-9_]+"
    r"|github\.event\.[a-zA-Z0-9_.]+"
    r"|github\.head_ref"
    r")\s*\}\}"
)


def files_to_check() -> list[Path]:
    targets: list[Path] = []
    action_yml = ROOT / "action.yml"
    if action_yml.exists():
        targets.append(action_yml)
    workflows = ROOT / ".github" / "workflows"
    if workflows.is_dir():
        targets.extend(sorted(p for p in workflows.iterdir() if p.suffix in {".yml", ".yaml"}))
    actions = ROOT / ".github" / "actions"
    if actions.is_dir():
        targets.extend(sorted(actions.rglob("action.yml")))
        targets.extend(sorted(actions.rglob("action.yaml")))
    return targets


def lint_file(path: Path) -> list[tuple[int, str]]:
    issues: list[tuple[int, str]] = []
    lines = path.read_text().splitlines()

    in_run_block = False
    run_key_indent = -1

    for i, line in enumerate(lines, start=1):
        indent = len(line) - len(line.lstrip(" "))

        if in_run_block:
            if line.strip() == "":
                continue
            if indent <= run_key_indent:
                in_run_block = False
            else:
                if FORBIDDEN_IN_RUN.search(line):
                    issues.append(
                        (
                            i,
                            "untrusted context expression in `run:` body — "
                            "route through env: and use as a quoted bash variable",
                        )
                    )
                continue

        m_uses = USES_RE.match(line)
        if m_uses:
            ref = m_uses.group(1)
            if not (ref.startswith("./") or ref.startswith("docker://")):
                if not SHA_RE.search(ref):
                    issues.append(
                        (
                            i,
                            f"action ref `{ref}` is not pinned to a 40-char commit SHA",
                        )
                    )
            continue

        m_block = RUN_BLOCK_RE.match(line)
        if m_block:
            in_run_block = True
            run_key_indent = len(m_block.group(1))
            continue

        m_inline = RUN_INLINE_RE.match(line)
        if m_inline and FORBIDDEN_IN_RUN.search(m_inline.group(2)):
            issues.append(
                (
                    i,
                    "untrusted context expression in single-line `run:` — "
                    "route through env: and use as a quoted bash variable",
                )
            )

    return issues


def main() -> int:
    failed = False
    for path in files_to_check():
        rel = path.relative_to(ROOT)
        for lineno, msg in lint_file(path):
            print(f"::error file={rel},line={lineno}::{msg}")
            failed = True
    if not failed:
        print("lint_actions.py: all action refs SHA-pinned and no untrusted context in run: bodies")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
