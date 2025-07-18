from __future__ import annotations

import ast
import json
from operator import itemgetter
from pathlib import Path

from more_itertools.more import map_reduce


def title2image():
    start_wars, rots, hp = tuple(
        map(
            ast.literal_eval,
            Path("harry_potter_vs_ROTS.txt").read_text().splitlines(),
        )
    )
    title2ulr = map_reduce(
        map(json.loads, Path("classified_memes.txt").read_text().splitlines()),
        keyfunc=itemgetter("title"),
        valuefunc=itemgetter("url"),
        reducefunc=itemgetter(0),
    )
    print("=== Harry Potter ===")
    print(len(hp), "\n".join(f"'{title}', {title2ulr[title]}" for title in hp))
    print("=== ROTS ===")
    print(
        len(rots),
        "\n".join(f"'{title}', {title2ulr[title]}" for title in rots),
    )
    print("=== Start Wars ===")
    print(
        len(start_wars),
        "\n".join(f"'{title}', {title2ulr[title]}" for title in start_wars),
    )


if __name__ == "__main__":
    title2image()
