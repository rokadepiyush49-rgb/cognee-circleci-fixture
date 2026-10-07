# congee-test-runs

A small repo whose CircleCI pipelines are used to test the cognee CircleCI connector ([#4710](https://github.com/topoteretes/cognee/issues/4710)). The tests are broken on purpose.

## What each branch produces

| Branch | Pipeline | Tests in the connector |
|---|---|---|
| `main` | Failed: 3 failing tests in `test`, `smoke` fails with no test results, `deploy` never runs | Failure output, no log text, failed job with nothing to report |
| `green` | All jobs pass | Status lines only, no tests fetched |
| `many-failures` | 28 failing tests in one job | Cap on failing tests per job |
| `slow` | `build-and-test` plus a job that runs about 5 min | Running at sync time → re-checked → final status |
| `hold` | `build-and-test` plus a workflow waiting on manual approval | `on_hold` pipeline that never finishes |

## Setup

1. Create an empty public GitHub repo (this one is `rokadepiyush49-rgb/congee-test-runs`) and push this folder to `main`:

   ```bash
   git init -b main && git add . && git commit -m "CircleCI connector fixture" && git remote add origin https://github.com/rokadepiyush49-rgb/congee-test-runs.git && git push -u origin main
   ```

2. In CircleCI, open **Projects → Set Up Project**, pick the repo, and choose the option that uses the existing `.circleci/config.yml` on `main`.
3. Create a token under **User Settings → Personal API Tokens** and export it:

   ```bash
   export CIRCLECI_TOKEN=...
   ```

4. Find the project slug under **Project Settings → Overview**. It's `gh/<you>/<repo>` for the GitHub OAuth integration, or `circleci/<org-id>/<project-id>` for the GitHub App integration. Export it:

   ```bash
   export SLUG=gh/rokadepiyush49-rgb/congee-test-runs
   ```

5. Create the other branches. Each one gets an empty commit so the push always starts a pipeline:

   ```bash
   for b in green many-failures slow hold; do git checkout -b $b main && git commit --allow-empty -m "trigger $b" && git push -u origin $b; done; git checkout main
   ```

All jobs use the `small` Docker resource class, so a full round uses only a few credits on the free plan. The `slow` job uses the most (about 5 minutes).

## Save real API responses as test fixtures

Run these after the pipelines exist. The connector's fake client can then return real response shapes.

```bash
mkdir -p fixtures && curl -s -H "Circle-Token: $CIRCLECI_TOKEN" "https://circleci.com/api/v2/project/$SLUG/pipeline" > fixtures/pipelines.json
```

Then follow the ids by hand: take a pipeline id from `fixtures/pipelines.json`, then a workflow id, then a job number.

```bash
curl -s -H "Circle-Token: $CIRCLECI_TOKEN" "https://circleci.com/api/v2/pipeline/<pipeline-id>/workflow" > fixtures/workflows.json
```

```bash
curl -s -H "Circle-Token: $CIRCLECI_TOKEN" "https://circleci.com/api/v2/workflow/<workflow-id>/job" > fixtures/jobs.json
```

```bash
curl -s -H "Circle-Token: $CIRCLECI_TOKEN" "https://circleci.com/api/v2/project/$SLUG/<job-number>/tests" > fixtures/tests.json
```

## Things to confirm against the real API

These are the behaviours the connector depends on. Check them here rather than assuming.

- [ ] The status of `deploy` on `main` when a job it requires failed (`blocked`? `not_run`?)
- [ ] What the tests endpoint returns for `smoke` (failed, no `store_test_results`): an empty list, or an error?
- [ ] Whether each test item has `file`, `name`, `classname`, `message` and `result` set (the config uses xunit1 so `file` is filled in)
- [ ] The workflow status on `hold` before anyone approves (`on_hold`), and after approving
- [ ] The workflow status on `slow` while the job is running (`running`)
- [ ] What `/project/$SLUG/pipeline` returns after you stop building the project in CircleCI (404?). The delete logic depends on this.
- [ ] Whether `?branch=green` filters the pipeline list as expected
