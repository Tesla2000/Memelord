from __future__ import annotations

import json
from operator import itemgetter
from pathlib import Path

from litellm import completion
from more_itertools import batched
from more_itertools.more import map_reduce
from pydantic import BaseModel
from pydantic import Field

BATCH_SIZE = 20


def harry_potter_vs_ROTS():
    start_wars, rots, hp = set(), set(), set()
    unique_memes = map_reduce(
        map(json.loads, Path("classified_memes.txt").read_text().splitlines()),
        keyfunc=itemgetter("hash"),
        valuefunc=itemgetter("title"),
        reducefunc=itemgetter(0),
    ).values()
    for batch_number, meme_batch in enumerate(
        batched(unique_memes, BATCH_SIZE), 1
    ):
        response = completion(
            "gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Classify a group of memes into categories. You will be given meme titles\nMEMES:\n"
                        + "\n".join(meme_batch)
                    ),
                }
            ],
            temperature=0.0,
            response_format=_GroupedMemes,
        )
        grouped_memes = _GroupedMemes.model_validate_json(
            response.choices[0].model_extra["message"].content
        )
        start_wars.update(grouped_memes.star_wars)
        start_wars.update(grouped_memes.rots)
        rots.update(grouped_memes.rots)
        hp.update(grouped_memes.harry_potter)
        print(
            batch_number,
            len(start_wars),
            len(rots),
            len(hp),
            start_wars,
            rots,
            hp,
        )
    Path("harry_potter_vs_ROTS.txt").write_text(
        "\n".join(map(str, (start_wars, rots, hp)))
    )


class _GroupedMemes(BaseModel):
    star_wars: list[str] = Field(
        default_factory=list,
        description="List of meme names with star wars as a source",
    )
    rots: list[str] = Field(
        default_factory=list,
        description="List of meme names with revenge of the sith as a source",
    )
    harry_potter: list[str] = Field(
        default_factory=list,
        description="List of meme names with harry potter as a source",
    )
    neither: list[str] = Field(
        default_factory=list,
        description="List of meme names with other sources",
    )


if __name__ == "__main__":
    harry_potter_vs_ROTS()
