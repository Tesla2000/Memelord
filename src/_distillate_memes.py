from __future__ import annotations

import json
from collections.abc import Collection
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

from _config import Config
from litellm import completion
from more_itertools import batched
from pydantic import BaseModel


def distillate_memes(
    grouped_memes: Collection[Collection[str]],
    needed_distillations: int,
    initial_group_size: int,
    config: Config,
) -> list[tuple[str]]:
    for distillation_pass in range(needed_distillations):
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    _filter_memes,
                    group,
                    (
                        config.initial_model
                        if distillation_pass < config.initial_model_passes
                        else config.final_model
                    ),
                    config,
                )
                for group in batched(grouped_memes, initial_group_size)
            ]
            distilled_memes = []
            for future in as_completed(futures):
                distilled_memes.extend(future.result())
        grouped_memes = distilled_memes
    return distilled_memes


def _filter_memes(
    group: Collection[Collection[str]], model_name: str, config: Config
) -> tuple[tuple[str], ...]:
    group_str = "\n".join(map(str, group))
    response = completion(
        model_name,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Here is the list of meme images with the title which one is the best response to: '{config.message}'. Return up to {config.n_results} best image urls\n{group_str}"
                ),
            }
        ],
        temperature=config.temperature,
        response_format=_MemeTitles,
    )
    response_titles = json.loads(response.choices[0]["message"]["content"])[
        "titles"
    ]
    return tuple(
        (title,)
        for title in filter(
            frozenset(chain.from_iterable(group)).__contains__, response_titles
        )
    )


class _MemeTitles(BaseModel):
    titles: list[str]
