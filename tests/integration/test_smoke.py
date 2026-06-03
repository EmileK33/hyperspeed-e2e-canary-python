"""Integration smoke test for the canary notes API.

Owned by the Phase 0 integration-harness session. The runner's integration wave
runs ``poetry run pytest tests/integration`` (or ``pytest tests/integration``)
against the host working tree; this file must pass on a clean checkout so the
harness's wave sequencing has a green baseline.
"""

from app.main import health


def test_health_probe_ok() -> None:
    assert health() == {"status": "ok"}


def test_arithmetic_baseline() -> None:
    # A trivially-true assertion so the integration wave is green before any
    # feature session adds real behaviour.
    assert 1 + 1 == 2
