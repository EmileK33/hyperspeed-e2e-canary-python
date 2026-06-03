"""Canary notes API package.

Intentionally near-empty. The canned source specs in ``../specs`` describe what
sessions should build; the fixture's starting state is "fresh poetry init +
pytest + one passing integration smoke test". Sessions own concrete modules
under ``app/`` so they can add top-level exports without colliding on this stub.
"""

__version__ = "0.0.1"
