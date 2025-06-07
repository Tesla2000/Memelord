from itertools import chain
from pathlib import Path

from config_parser import ConfigCreator

from _calculate_process_values import calculate_process_values
from _config import Config
from _distillate_memes import distillate_memes
from _group_memes import group_memes
from _load_memes import load_memes
from _save_memes import gather_memes


def main():
    config = ConfigCreator().create_config(Config)
    if config.re_fetch or not Path(config.classified_file).exists():
        gather_memes(config)
    memes = tuple(load_memes(config))
    grouped_memes = tuple(group_memes(memes).values())
    initial_group_size, needed_distillations = calculate_process_values(grouped_memes, config)
    distilled_memes = distillate_memes(needed_distillations, initial_group_size, config)
    distilled_meme_titles = frozenset(chain.from_iterable(distilled_memes))
    print(tuple(image for image in memes if image.title in distilled_meme_titles))



if __name__ == "__main__":
    main()
