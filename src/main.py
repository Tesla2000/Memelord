import argparse
import json
from itertools import islice
from pathlib import Path

from _create_utterances import create_utterances
from _group_memes import group_memes
from _load_memes import load_memes
from _memes import MemeImage
from classify_meme import classify_memes
from meme_scraper import scrape_memes


def main():
    parser = argparse.ArgumentParser(description='Process memes with custom folder locations.')
    parser.add_argument('--meme-folder', type=str, default='memes',
                        help='Directory containing meme files (default: memes)')
    parser.add_argument('--classified-file', type=str, default='classified_memes.txt',
                        help='File for storing classified meme files (default: classified_memes)')
    args = parser.parse_args()
    # meme_folder = Path(args.meme_folder)
    # meme_folder.mkdir(exist_ok=True, parents=True)
    # Path(args.classified_file).write_text("\n".join(json.dumps(meme._asdict()) for meme in classify_memes(scrape_memes(meme_folder))))
    memes = tuple(load_memes(Path(args.classified_file)))
    meme_groups = group_memes(memes)
    meme_utterances = {str((meme_url, *meme_titles)): create_utterances(meme_titles) for meme_url, meme_titles in islice(meme_groups.items(), 10)}
    print(json.dumps(meme_utterances, indent=2, default=str))


if __name__ == "__main__":
    main()
