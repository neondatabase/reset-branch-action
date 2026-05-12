# Security policy

## Reporting a vulnerability

Please report suspected security vulnerabilities in this action **privately**, not via a public GitHub issue.

- Email: `security@neon.tech`
- GitHub: use [private vulnerability reporting](https://github.com/neondatabase/reset-branch-action/security/advisories/new)

We aim to acknowledge reports within 2 business days.

## Scope

This repository ships a composite GitHub Action that runs in the consumer's CI with the consumer's `NEON_API_KEY`. Security-relevant categories include:

- Shell injection or command injection through any action input.
- Privilege escalation against the consumer's CI runner or secrets.
- Supply-chain issues with the action's runtime dependencies (`neonctl` and its transitive npm dependencies).
- Mutation of release tags (`v1`, `v1.x`, `vX.Y.Z`) to point at unintended commits.

## Pinning

Consumers should pin this action by commit SHA, not by tag. See the "Pinning and security" section of the [README](./README.md) for the recommended pattern.

## Disclosure

We coordinate with the reporter on a disclosure timeline. Default is 90 days from acknowledgement, or sooner once a fix is shipped and consumers have had time to upgrade.
