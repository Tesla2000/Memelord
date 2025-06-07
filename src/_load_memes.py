import json
from pathlib import Path
from typing import Generator

from _memes import MemeImage


def load_memes(filepath: Path) -> Generator[MemeImage, None, None]:
    yield from (MemeImage(**json.loads(line)) for line in filepath.read_text().splitlines())
