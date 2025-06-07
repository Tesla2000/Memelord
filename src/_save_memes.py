import json
from pathlib import Path
from typing import Iterable, NamedTuple


def save_memes(memes: Iterable[NamedTuple], filepath: Path):
    filepath.write_text("\n".join(json.dumps(meme._asdict()) for meme in memes))
