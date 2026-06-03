# Python canary project — `hyperspeed-canary-notes`

Tiny Poetry notes API. Exists **only** as the python target project that
`tests/e2e/run-canary.mjs --fixture python` exercises the Track B Node runner
against (issue #40 / Track D). It is the python analog of the node
`../canary-project` and is the fixture for the #125 follow-up scenarios:

- **`pyproject-reconcile`** — the python analog of `branch-freshness`. Several
  same-wave sessions each add a distinct dependency to the one shared
  `pyproject.toml`; the runner's pre-PR reconcile (#125 Item 1,
  `mergePyprojectToml`) must union them so none is dropped.
- **`test-cwd`** — a session's `test.cmd` runs from `test.cwd` (#125 Item 4),
  never via a `cd …` prefix.

This is not a published package. It is a fixture. Treat it like one:

- `pyproject.toml`, `poetry install`, `poetry run pytest`, and
  `poetry run pytest tests/integration` are real and must work — that is the
  whole point.
- `app/` is intentionally near-empty. The canned source specs in `../specs/`
  describe what sessions should build; the canary's starting state is "fresh
  poetry init + pytest + one passing integration smoke test".
- Session output never lands here. The harness copies this dir into a scratch
  checkout of the throwaway test repo on every run.

## Toolchain requirement

Unlike the node fixture (where the #120 reconcile uses lock-free `scripts`
entries), the python reconcile may **relock** (`poetry lock` / `pip install`)
after unioning `pyproject.toml`. The harness host — and the throwaway repo's CI
image — must therefore have **`poetry`** (and a `python` matching the declared
floor) on `PATH`. The `pyproject-reconcile` scenario self-skips with guidance
when `poetry` is absent rather than producing a false failure.

The throwaway repo's `.github/workflows/session-tests.yml` must do python setup
(`actions/setup-python` + `pip install poetry` + `poetry install`) so the
session PRs pass CI and auto-merge. See [tests/e2e/README.md](../README.md)
"Python fixture (`--fixture python`)" for the workflow YAML.

To use directly (sanity check the scripts work):

```bash
cd tests/e2e/python-canary-project
poetry install
poetry run pytest                      # all tests
poetry run pytest tests/integration    # integration gate only
```

See [tests/e2e/README.md](../README.md) for the full harness flow.
