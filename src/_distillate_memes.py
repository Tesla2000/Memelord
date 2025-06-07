import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import chain
from typing import Collection

from litellm import completion
from more_itertools import batched
from pydantic import BaseModel

from _config import Config


def distillate_memes(needed_distillations: int, initial_group_size: int, config: Config) -> list[tuple[str]]:
    for distillation_pass in range(needed_distillations):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(_filter_memes, group, "I don’t think this software update will work.", config.n_results, (config.initial_model if distillation_pass < config.initial_model_passes else config.final_model)) for group in
                       batched(grouped_memes, initial_group_size)]
            distilled_memes = []
            for future in as_completed(futures):
                distilled_memes.extend(future.result())
        grouped_memes = distilled_memes
    return distilled_memes


def _filter_memes(group: Collection[Collection[str]], message: str, n_results: int, model_name: str) -> tuple[tuple[str], ...]:
    group_str = '\n'.join(map(str, group))
    response = completion(
        model_name,
        messages=[
            {
                "role": "user",
                "content": f"Here is the list of meme images with the title which one is the best response to: '{message}'. Return up to {n_results} best image urls\n{group_str}",
            }
        ],
        temperature=0.0,
        response_format=_MemeTitles
    )
    response_titles = json.loads(response.choices[0]["message"]["content"])["titles"]
    return tuple((title,) for title in filter(frozenset(chain.from_iterable(group)).__contains__, response_titles))

class _MemeTitles(BaseModel):
    titles: list[str]

