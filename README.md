# 🔄 Neon Reset Branch Action

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./docs/logos/neon-logo-dark.svg">
    <img alt="Neon logo" src="./docs/logos/neon-logo-light.svg">
  </picture>
</p>

This action resets a specified Neon branch to the latest data from its parent branch. Future releases will support other types of branch resets. For example, rewind a branch to an earlier point in time.

It is useful in workflows where you need to refresh a development or testing branch with the most recent data from its upstream parent.

## Setup

Using the action requires adding a Neon API key to your GitHub Secrets. There are two ways you can perform this setup:

- **Using the Neon GitHub Integration** (recommended 👍) — this integration connects your Neon project to your GitHub repository, creates an API key, and sets the API key in your GitHub repository for you. See [Neon GitHub Integration](https://neon.tech/docs/guides/neon-github-integration) for instructions.
- **Manual setup** — this method requires obtaining a Neon API key and configuring it manually in your GitHub repository.

  1. **Obtain a Neon API key.** See [Create an API key](https://neon.tech/docs/manage/api-keys#create-an-api-key) for instructions on the Neon documentation.
  2. In your GitHub repository, go to **Settings** and locate **Secrets and variables** at the bottom of the left sidebar.
  3. Click **Actions** > **New repository secret**.
  4. Name the secret `NEON_API_KEY` and paste your API key in the **Value** field.
  5. Click **Add secret**.

## Usage

The following fields are required to run the Reset Branch action:

- `project_id` — The Neon project ID. If you have the Neon GitHub Integration installed, you can specify `${{ vars.NEON_PROJECT_ID }}`. You can find the project ID of your Neon project on the Settings page of your Neon console.
- `api_key` — The Neon API key for your Neon project or organization. If you have the GitHub integration installed, specify `${{ secrets.NEON_API_KEY }}`.
- `branch` — Specifies the branch to reset. You can use either the branch name or the branch ID.

Setup the action in your workflow:

```yml
steps:
  - uses: neondatabase/reset-branch-action@v1
    id: reset-branch # Step ID to reference outputs
    with:
      project_id: your_neon_project_id
      parent: true # always set to true to reset to the latest of the parent branch as only resetting to parent is supported for now
      branch: actions_reusable # Specify branch name or ID here
      api_key: ${{ secrets.NEON_API_KEY }}
```

Alternatively, you can use `${{ vars.NEON_PROJECT_ID }}` to get your `project_id`. If you have set up the [Neon GitHub Integration](https://neon.tech/docs/guides/neon-github-integration), the `NEON_PROJECT_ID` variable will be defined as a variable in your GitHub repository.

If you need to connect to the reset branch in subsequent steps, you can use the outputs of this action, such as the updated database connection URL. See the [Outputs](#outputs) section below for details.

## Outputs

The action provides the following outputs:

- `branch_id` — The ID of the reset Neon branch.
- `db_url` — The DATABASE_URL connection string for the branch after reset.
- `db_url_with_pooler` — DATABASE_URL with connection pooling enabled for the branch after reset.
- `host` — The host address of the branch after reset.
- `host_with_pooler` — The host address with connection pooling enabled for the branch after reset.
- `password` — The password for connecting to the branch database after reset.

### Example Workflow

Here is an example of a complete GitHub Actions workflow that resets a Neon branch:

```yml
name: Neon Github Actions Reset Branch

on:
  # You can modify the following line to trigger the workflow on a different event, such as `push` or `pull_request`, as per your requirements. We have used `workflow_dispatch` for triggering the action in this example.
  workflow_dispatch:

jobs:
  Reset-Neon-Branch:
    runs-on: ubuntu-24.04
    steps:
      - uses: neondatabase/reset-branch-action@v1
        id: reset-branch
        with:
          project_id: ${{ vars.NEON_PROJECT_ID }}
          branch: actions_reusable # Replace with the branch name or ID you want to reset
          parent: true # always set to true to reset to the latest of the parent branch as only resetting to parent is supported for now
          api_key: ${{ secrets.NEON_API_KEY }}
      - run: echo Branch ID ${{ steps.reset-branch.outputs.branch_id }}
```

## Advanced usage

You can further customize the action using these optional inputs:

- **`cs_role_name`**: Customize the database role name in the output connection strings. If not specified, the default role associated with the branch will be used.
- **`cs_database`**: Customize the database name in the output connection strings. If not specified, the default database name of the branch will be used.
- **`cs_prisma`**: Set to `true` to format the output connection strings for Prisma. Defaults to `false`.
- **`cs_ssl`**: Control the `sslmode` in the output connection strings. Supported values: `"require"`, `"verify-ca"`, `"verify-full"`, `"omit"`. Defaults to `"require"`.

If you donot provide any values for these optional fields, the action uses the following defaults for connection string outputs:

- `cs_role_name`: Default role of the branch.
- `cs_database`: Default database of the branch.
- `cs_prisma`: `false`
- `cs_ssl`: `require`

Supported parameters:

| Field          | Required/optional | Default value                      | Description                                                                                                           |
| -------------- | ----------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `project_id`   | required          | n/a                                | The ID of your Neon project.                                                                                          |
| `api_key`      | required          | n/a                                | Your Neon API key.                                                                                                    |
| `branch`       | required          | n/a                                | The name or ID of the branch to reset.                                                                                |
| `api_host`     | optional          | `https://console.neon.tech/api/v2` | The Neon API host URL.                                                                                                |
| `cs_role_name` | optional          | _Default branch role_              | Database role name for the output connection strings.                                                                 |
| `cs_database`  | optional          | _Default branch database_          | Database name for the output connection strings.                                                                      |
| `cs_prisma`    | optional          | `false`                            | Whether to format connection strings for Prisma.                                                                      |
| `cs_ssl`       | optional          | `require`                          | `sslmode` for the output connection strings. Supported values: `"require"`, `"verify-ca"`, `"verify-full"`, `"omit"`. |

---

## Other Actions

Check out other Neon GitHub Actions:

- [Create Branch Action](https://github.com/neondatabase/create-branch-action)
- [Delete Branch Action](https://github.com/neondatabase/delete-branch-action)
- [Schema Diff Action](https://github.com/neondatabase/schema-diff-action)
