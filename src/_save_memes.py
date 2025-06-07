from __future__ import annotations

import json
from pathlib import Path

from _classify_meme import classify_memes
from _config import Config
from _meme_scraper import scrape_memes


def gather_memes(config: Config) -> None:
    Path(config.classified_memes_file).write_text(
        "\n".join(
            json.dumps(meme._asdict())
            for meme in classify_memes(scrape_memes(config.meme_folder))
        )
    )
