from __future__ import annotations

from typing import NamedTuple


class MemeImage(NamedTuple):
    title: str
    url: str
    hash: str
    is_response: bool = False

    def __hash__(self):
        return hash(self.hash)

    def __repr__(self):
        return f"{self.title} {self.url}"
