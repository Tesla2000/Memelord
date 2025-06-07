from typing import NamedTuple


class MemeImage(NamedTuple):
    title: str
    url: str
    hash: str
    # page: int
    is_response: bool = False

    def __hash__(self):
        return hash(self.hash)