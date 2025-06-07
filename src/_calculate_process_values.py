from __future__ import annotations

from collections.abc import Sized
from math import ceil
from math import floor
from math import log

from _config import Config


def calculate_process_values(
    grouped_memes: Sized, config: Config
) -> tuple[int, int]:
    n_memes = len(grouped_memes)
    needed_distillations = abs(floor(log(n_memes, config.distillation_factor)))
    passed_fraction = config.n_results / n_memes
    return (
        ceil(
            config.n_results * passed_fraction ** (-1 / needed_distillations)
        ),
        needed_distillations,
    )
