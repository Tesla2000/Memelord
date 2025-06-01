import hashlib
from pathlib import Path
from typing import NamedTuple

import requests
from PIL import Image
from bs4 import BeautifulSoup


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
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        # Resize to a small size for faster hashing
        img = img.resize((8, 8), Image.LANCZOS)
        # Convert to grayscale
        img = img.convert('L')
        # Get pixel data
        pixels = list(img.getdata())
        # Compute average pixel value
        avg = sum(pixels) / len(pixels)
        # Compute hash: 1 if pixel value >= average, 0 otherwise
        bits = ''.join('1' if pixel >= avg else '0' for pixel in pixels)
        # Convert bits to hexadecimal
        return hashlib.sha256(bits.encode()).hexdigest()
    except Exception as e:
        print(f"Error hashing image {image_url}: {e}")
        return None



class MemeImage(NamedTuple):
    title: str
    url: str
    hash: str

def scrape_memes():
    """Scrape meme templates from imgflip.com."""
    base_url = "https://imgflip.com/memetemplates"
    memes = []  # Dictionary to store image hash -> list of names

    for page in range(1, 3):
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}...")
        content = fetch_page(url)
        soup = BeautifulSoup(content, 'html.parser')

        # Find all meme templates on the page
        meme_templates = soup.select('.mt-box')

        if not meme_templates:
            print(f"No more meme templates found on page {page}. Stopping.")
            break

        for template in meme_templates:
            # Extract meme name
            name_elem = template.select_one('.mt-title')
            if not name_elem:
                continue

            name = name_elem.text.strip()

            # Extract image URL
            img_elem = template.select_one('.shadow')
            if not img_elem or not img_elem.has_attr('src'):
                continue

            img_url = img_elem['src']
            if not img_url.startswith('http'):
                img_url = 'https:' + img_url

            # Hash the image to check for duplicates
            img_hash = hash_image(img_url)
            if not img_hash:
                continue
            memes.append(MemeImage(name, img_url, img_hash))
        Path(f"memes/{page}.txt").write_text("\n".join(map(str, memes)))
        # Check if there's a next page
        next_page = soup.select_one('.pager-next')
        if not next_page or 'disabled' in (next_page.get('class') or []):
            print("No more pages. Stopping.")
            break


if __name__ == "__main__":
    scrape_memes()
