import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE / "src" / "backend" / "engine"))
sys.path.insert(0, str(BASE / "src" / "backend"))

CZ_API = BASE.parent / "Vývoj a rešerše s OpenCode" / "cz_pension_api"
if CZ_API.exists():
    sys.path.insert(0, str(CZ_API))
