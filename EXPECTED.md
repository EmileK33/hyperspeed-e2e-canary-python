# Expected outputs — Python canary build plan

This file documents what the python canary's source specs (`specs/`) should
produce when run through `hyperspeed --generate-build-plan` and then through
`agents/build-plan/runner-template/run-build.mjs` with `--fixture python`.

The harness (`tests/e2e/run-canary.mjs`) asserts against this contract. If the
build-plan agent legitimately changes its session naming, file ownership
splits, or wave ordering, **update this file in the same commit** so the
contract stays meaningful.

## Sessions

Five sessions across three phases (phase 0 = integration harness + two feature
phases). Concrete IDs may shift if the agent renames them; assertions match by
*count per phase* and *file ownership* rather than literal IDs where possible.

| Phase | Expected sessions | What they own | Manual ACs |
| --- | --- | --- | --- |
| 0 | 1 (S0-A) | `pyproject.toml`, `tests/integration/test_smoke.py`, `app/main.py` | 0 |
| 1 | 2 (S1-A, S1-B) | `app/store.py` + `app/models.py` | 0 |
| 2 | 2 (S2-A, S2-B) | `app/routes/notes.py` + `app/routes/status.py` | **1** (`US-005 AC-3`, canary brand color `#2ec4b6`) |

Total sessions: **5**. Total PRs opened on a clean run: **5**.

## Waves

Manifest waves should interleave feature and integration:

```
W0  feature      phase 0 — 1 session
W1  integration  integration-0  → poetry run pytest tests/integration
W2  feature      phase 1 — 2 sessions
W3  integration  integration-1  → poetry run pytest tests/integration
W4  feature      phase 2 — 2 sessions
W5  integration  integration-2  → poetry run pytest tests/integration
```

Integration command: `poetry run pytest tests/integration` (a bare
`pytest tests/integration` is an equally valid expression of the same gate).

## Toolchain (requirements block)

The generated `run-manifest.json` must declare a **python** runtime so the
ecosystem-keyed reconcile (#125 Item 1) treats `pyproject.toml` conflicts as
python:

- `requirements.runtimes[]` includes `{ name: "python", version: "3.11" }`.
- `requirements.hostBinaries[]` includes `poetry` (and `pytest` via the test
  commands).
- `projectManifestStub.path` is `pyproject.toml` (ecosystem inferred as python).
- No `requirements.services[]` (the canary uses no Postgres/Redis).

## PR titles

Each session opens one PR titled `<session-id>: autonomous build`,
e.g. `S2-A: autonomous build`. Branch: `bp/<run-id>/<session-id>`.

## Manual ACs

Exactly one session — the one owning `app/routes/status.py` (US-005) — should
carry a `[MANUAL]` AC for the canary brand color `#2ec4b6`.

## Why this fixture exists

The node canary (`../canary-project`) cannot exercise the **python** dependency
reconcile (Item 1: `mergePyprojectToml`) or a python `test.cwd` on a real
toolchain. This fixture is the python analog: a Poetry project whose Phase 0
owns `pyproject.toml`, so that the `pyproject-reconcile` scenario can make
several same-wave sessions each add a dependency to the one shared manifest and
prove the 3-way union drops none.

## Notes on robustness

The build-plan agent is non-deterministic. To keep the harness from flaking:

- Match session count per phase, not exact session names.
- Match PR title pattern (`/^S\d+-[A-Z]: autonomous build$/`).
- Match the `[MANUAL]` AC by the literal `#2ec4b6` token (a unique teal chosen
  so it survives agent rewording).
- Tolerate the integration wave running `poetry run pytest tests/integration`
  or `pytest tests/integration`.
