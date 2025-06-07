from __future__ import annotations

from collections.abc import Generator
from collections.abc import Iterable
from functools import lru_cache

import tqdm
from _memes import MemeImage


@lru_cache
def nlp():
    import spacy

    return spacy.load("en_core_web_trf")


def classify_memes(
    memes: Iterable[MemeImage],
) -> Generator[MemeImage, None, None]:
    return (
        yield from (
            MemeImage(
                *meme[:-1],
                is_response=any(
                    token.pos_ == "AUX"
                    or token.text.lower() in ("x", "y")
                    or (
                        token.pos_ == "VERB"
                        and not token.text.lower().endswith("ing")
                    )
                    for token in nlp()(meme.title)
                ),
            )
            for meme in tqdm.tqdm(memes)
        )
    )
