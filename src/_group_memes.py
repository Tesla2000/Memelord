from typing import Iterable

from more_itertools import map_reduce

from _memes import MemeImage


def group_memes(memes: Iterable[MemeImage]) -> dict[str, frozenset[str]]:
    return {memes[0].url: frozenset(meme.title for meme in memes) for memes in map_reduce(filter(lambda meme: meme.is_response, memes), lambda meme: meme.hash).values()}
