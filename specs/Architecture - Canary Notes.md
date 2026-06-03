# Architecture — Canary Notes API

Python 3.11 · Poetry + pytest · no database (in-memory store). A build-plan
**fixture** shaped to decompose into a Phase 0 integration harness + 2 feature
phases with disjoint file ownership. See `../EXPECTED.md` for the session/wave
contract.

## Stack

- **Runtime:** Python 3.11, packaged with Poetry (`pyproject.toml`).
- **HTTP:** a minimal WSGI app (stdlib `wsgiref` for the fixture) with a JSON
  helper. No framework dependency is required by the fixture.
- **Datastore:** in-memory dict-backed store — **no Postgres, no services**. This
  is deliberate: it exercises the "services absent" generation path.
- **Tests:** pytest. Integration tests live under `tests/integration/`.

## Module layout (file ownership — one owner each)

| Area | Files | Phase |
|---|---|---|
| Integration harness | `tests/integration/test_smoke.py`, `pyproject.toml`, `app/main.py` | 0 |
| Models | `app/models.py` | 1 |
| Store | `app/store.py` | 1 |
| Note routes | `app/routes/notes.py` | 2 |
| Status route | `app/routes/status.py` | 2 |

## Shared resources

- **`conftest.py` / pytest configuration** — Python's shared test registry;
  single-owner (Phase 0), never edited by feature sessions.
- No shared mutable runtime substrate (the store is process-local + in-memory),
  so there is no DB-coordination contract to declare.

## Toolchain

- `pyproject.toml` (Poetry) owns deps: `pytest` (dev). Feature sessions may add
  pure-python deps; the runner's `mergePyprojectToml` 3-way-unions them (#125
  Item 1).
- Integration command: `poetry run pytest tests/integration`.
- `requirements.runtimes[]` must declare `python` so the ecosystem-keyed
  reconcile treats `pyproject.toml` conflicts as python.

## Cross-session contracts

- `app/routes/*` import `Note` + store functions from `app/models.py` and
  `app/store.py` (Phase 1 → Phase 2 dependency; producer phase precedes consumer
  phase).
- Because Python is dynamically typed, the plan-time contract proof degrades to
  ADVISORY "unverified" — the CI pytest gate proves cross-module compatibility at
  build time (#144 Decision B).
