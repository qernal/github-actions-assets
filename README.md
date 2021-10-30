# GitHub Actions: Asset

![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)

Github action to fetch private releases/packages/assets, this provides fetching with the following features;

- Auto extract archives

## Workflow configuration

To use this action, define it in your workflow;

```yaml
on: [push, pull_request]

jobs:
  lint:
    runs-on: self-hosted
    name: Fetch assets
    steps:
      - uses: actions/checkout@v2
      - uses: qernal/github-actions-assets@v1.0.0
```

### Action parameters

| Parameter | Description | Default | Required | Values |
| ---- | ---- | ---- | ---- | ---- |
| `tag` | Release tag to retrieve | _no default_ | Y | String |
| `repo_name` | Name of the repository to create release on | _no default_ | Y | String |
| `extract` | Automatically extract archives on download | false | N | Boolean |
| `output_dir` | Name of the repository to create release on | _no default_ | Y | String |
| `token` | GitHub PAT Token to access/create release | _no default_ | Y | String |

Example;

```yaml
    steps:
      - uses: actions/checkout@v2
      - uses: qernal/github-actions-rust-assets@v1.0.0
        with:
          tag: "abc_v1.6.3"
          repo_name: "me/repo"
          output_dir: "./output/"
          token: "${{ secrets.github_token }}"
```
## Manual runs

You can use the container without the context of the runner, and just run the container like so;

```bash
docker run --rm -v `pwd`:/github/workspace ghcr.io/qernal/gh-actions/assets-x86_64:main
```

Replace the `pwd` with your workspace if you're not running from the current directory

## Development

```bash
INPUT_TAG="abc_v1.0.0" INPUT_REPO_NAME="my-user/releases-repo" INPUT_TOKEN="xxxx" INPUT_BASE_DIR="./" INPUT_OUTPUT_DIR="./output/" INPUT_EXTRACT="true" python3 ./src/assets.py
```