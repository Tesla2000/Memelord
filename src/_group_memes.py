from __future__ import annotations

from collections.abc import Iterable

from _memes import MemeImage
from more_itertools import map_reduce


def group_memes(memes: Iterable[MemeImage]) -> dict[str, tuple[str, ...]]:
    return {
        memes[0].url: tuple(frozenset(meme.title for meme in memes))
        for memes in map_reduce(memes, lambda meme: meme.hash).values()
    }
