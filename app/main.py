"""Canary notes API entry point.

Kept deliberately tiny: the in-memory store and the route handlers are what the
build-plan sessions are expected to add (see ``../specs``). This module only
exposes a health probe so the integration smoke test has something to import
before any feature session lands.
"""


def health() -> dict[str, str]:
    """Liveness probe used by the integration smoke test."""
    return {"status": "ok"}
