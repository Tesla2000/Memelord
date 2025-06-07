import hashlib
import io
import json
from itertools import count
from pathlib import Path
from typing import Generator

import requests
from PIL import Image
from bs4 import BeautifulSoup

from _memes import MemeImage


def fetch_page(url):
    """Fetch a web page and return its content."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def hash_image(image_url):
    """Download an image and compute its hash."""
    response = requests.get(image_url)
    response.raise_for_status()
    img = Image.open(io.BytesIO(response.content))
    img = img.resize((8, 8), Image.LANCZOS)
    img = img.convert('L')
    pixels = list(img.getdata())
    avg = sum(pixels) / len(pixels)
    bits = ''.join('1' if pixel >= avg else '0' for pixel in pixels)
    return hashlib.sha256(bits.encode()).hexdigest()


def scrape_memes(memes_path: Path) -> Generator[MemeImage, None, None]:
    """Scrape meme templates from imgflip.com."""
    base_url = "https://imgflip.com/memetemplates"
    for page in count(1):
        memes = []
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}...")
        content = fetch_page(url)
        soup = BeautifulSoup(content, 'html.parser')

        meme_templates = soup.select('.mt-box')

        if not meme_templates:
            print(f"No more meme templates found on page {page}. Stopping.")
            break

        for template in meme_templates:
            name_elem = template.select_one('.mt-title')
            if not name_elem:
                continue

            name = name_elem.text.strip()

            img_elem = template.select_one('.shadow')
            if not img_elem or not img_elem.has_attr('src'):
                continue

            img_url = img_elem['src']
            if not img_url.startswith('http'):
                img_url = 'https:' + img_url

            img_hash = hash_image(img_url)
            if not img_hash:
                continue
            memes.append(MemeImage(name, img_url, img_hash)._asdict())
            yield MemeImage(name, img_url, img_hash)
        (memes_path / f"{page}.txt").write_text(
            "\n".join(map(json.dumps, memes)))
        next_page = soup.select_one('.pager-next')
        if not next_page or 'disabled' in (
                next_page.get('class') or []) or not memes:
            print("No more pages. Stopping.")
            break
