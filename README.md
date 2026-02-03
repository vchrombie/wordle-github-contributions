# wordle-github-contributions

Generates your monthly GitHub Contributions as a Wordle-style grid and can update a README section automatically.

---

## Usage

Add the markers to the README you want to update (for example `vchrombie/vchrombie/README.md`):

```md
<!-- wordle-github:start -->
<!-- wordle-github:end -->
```

Create a workflow file in that repository:

`.github/workflows/wordle-github.yml`

```yaml
name: Wordle GitHub Contributions

on:
  schedule:
    # at 08:00 on the 1st of every month
    - cron: "0 8 1 * *"
  workflow_dispatch:

jobs:
  update-contribution-grid:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: vchrombie/wordle-github-contributions@main
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          OUTPUT_FILE: README.md
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Update Wordle contributions"
```

The above job runs at 08:00 UTC, on the 1st of every month. You can change it as you wish based on the cron syntax.

It fetches your contribution data of the last month, generates the Wordle grid and updates the README content between the markers.

## Inputs

| Input Param    | Default Value                   | Description                                     |
| -------------- | ------------------------------- | ----------------------------------------------- |
| `GH_USERNAME`  | repository owner                | GitHub username whose contributions to fetch    |
| `TITLE`        | GitHub Contributions Wordle     | Heading text to include in the output           |
| `SHOW_MONTH`   | True                            | Include the month label in the output           |
| `OUTPUT_FILE`  | (empty)                         | Optional file path to update (e.g. `README.md`) |
| `MARKER_START` | <!-- wordle-github:start -->    | Start marker used when updating `OUTPUT_FILE`   |
| `MARKER_END`   | <!-- wordle-github:end -->      | End marker used when updating `OUTPUT_FILE`     |
| `SVG_FILE`     | wordle-github-contributions.svg | Optional file path to save the SVG image        |

## Outputs

The action exposes the markdown in the `content` output if you want to use it in another step.

```yaml
- uses: vchrombie/wordle-github-contributions@main
  id: wordle
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
- run: echo "${{ steps.wordle.outputs.content }}"
```

---

Made out of boredom on a Sunday evening.

## Environment Variables

| Variable   | Required | Description                         |
| ---------- | -------- | ----------------------------------- |
| `GH_TOKEN` | Yes      | GitHub token for GraphQL API access |

For local runs, you can copy `.env.example` to `.env` and fill in values.
