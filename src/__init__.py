from __future__ import annotations

import sys
from pathlib import Path

from _main import main

sys.path.insert(0, str(Path(__file__).parent))
__all__ = ["main"]
