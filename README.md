<p align="center">
  <img width="250px" src="https://user-images.githubusercontent.com/13738772/201432652-63a10fc1-a6a5-423f-8ee0-b18a11308077.svg" />
<p align="center">


## Reset a Neon Branch 🚀
This GitHub action resets a child branch with the latest data from its parent branch. Future releases will support other types of branch resets. For example, rewind a branch to an earlier point in time.

Here is an example of how to use it:

```yml
name: Reset Neon Branch with GitHub Actions Demo
run-name: Reset a Neon Branch 🚀
jobs:
  Reset-Neon-Branch:
    uses: neondatabase/reset-branch-action@v1
    with:
      project_id: rapid-haze-373089
      parent: true
      branch: child_branch
      api_key: {{ secrets.NEON_API_KEY }}
    id: reset-branch
  - run: echo branch_id ${{ steps.reset-branch.outputs.branch_id }}
```
### Input variables

- `project_id`: The ID of your Neon project. Find this value in the Neon Console on the **Settings** page.
- `parent`: If specified, the branch will be reset to the latest (HEAD) of parent branch.
- `branch`: The name or id of the branch to reset.
- `api_key`: An API key created in your Neon account. See [How to set up the NEON_API_KEY](#how-to-set-up-the-neon_api_key) for instructions.

### Outputs

```yaml
outputs:
  branch_id:
    description: 'Reset branch id'
    value: ${{ steps.reset-branch.outputs.branch_id }}
```
- `branch_id`: The ID of the newly reset branch.

## How to set up the NEON_API_KEY
Navigate to the [Developer Settings](https://console.neon.tech/app/settings/api-keys) page in the Neon Console. Generate a new API key if you don't have one already. It's important not to share the API key or expose it in your actions or code. This is why you need to add the API key to a new GitHub secret.

In your GitHub repo, go to `Settings` and locate `Secrets` at the bottom of the left sidebar. Click on `Actions` and then on the `New repository secret` button to create a new secret.
Name the secret `NEON_API_KEY` and paste the API key generated on the Neon console in the `Secret*` field, then press `Add secret` button.

See full documentation about managing API keys [here](https://neon.tech/docs/manage/api-keys).
