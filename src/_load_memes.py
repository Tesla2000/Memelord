import json
from typing import Generator

from _config import Config
from _memes import MemeImage


def load_memes(config: Config) -> Generator[MemeImage, None, None]:
    yield from filter(lambda meme_image: config.include_non_response or meme_image.is_response, (MemeImage(**json.loads(line)) for line in config.classified_memes_file.read_text().splitlines()))
