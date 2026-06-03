import sys
import os
# Ensure `app` is importable when pytest runs without the project installed as
# a package (e.g. after --seed-base replaces pyproject.toml with a generated
# stub that omits `packages = [{include="app"}]`).
sys.path.insert(0, os.path.dirname(__file__))
