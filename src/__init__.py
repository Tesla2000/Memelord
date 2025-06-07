import sys
from pathlib import Path
from main import main

sys.path.insert(0, str(Path(__file__).parent))
__all__ = ["main"]
