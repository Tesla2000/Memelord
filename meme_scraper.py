from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup
import json
import hashlib
import io
from PIL import Image
import re

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

def is_ai_related_meme(name):
    """
    Determine if a meme is related to AI technologies like langchain, pydantic, AI, or litellm.
    """
    # List of AI-related terms to check for
    ai_terms = [
        'langchain', 'pydantic', 'ai', 'artificial intelligence', 'litellm',
        'machine learning', 'ml', 'deep learning', 'neural network', 'gpt',
        'chatgpt', 'openai', 'llm', 'large language model'
    ]

    # Check if the meme name contains any of the AI-related terms
    name_lower = name.lower()
    return any(term in name_lower for term in ai_terms)

def is_text_response_meme(name):
    """
    Determine if a meme is a 'text response' type.
    Text response memes typically have patterns like "X, X Everywhere", "Always Has Been", etc.
    Also checks if the meme is related to AI technologies like langchain, pydantic, AI, or litellm.
    """
    # List of common text response meme patterns
    text_response_patterns = [
        r'.*\b(always has been)\b.*',
        r'.*\b(\w+,\s*\w+\s+everywhere)\b.*',
        r'.*\b(one does not simply)\b.*',
        r'.*\b(change my mind)\b.*',
        r'.*\b(am i the only one)\b.*',
        r'.*\b(is this a)\b.*',
        r'.*\b(not sure if)\b.*',
        r'.*\b(what if i told you)\b.*',
        r'.*\b(y u no)\b.*',
        r'.*\b(brace yourselves)\b.*',
        r'.*\b(that would be great)\b.*',
        r'.*\b(shut up and take my money)\b.*',
        r'.*\b(ain\'t nobody got time for that)\b.*',
        r'.*\b(i don\'t always)\b.*',
        r'.*\b(but when i do)\b.*',
        r'.*\b(you\'re gonna have a bad time)\b.*',
        r'.*\b(i\'ll have you know)\b.*',
        r'.*\b(why not both)\b.*',
        r'.*\b(look at all the)\b.*',
        r'.*\b(this is where i\'d put)\b.*',
        r'.*\b(if i had one)\b.*',
        r'.*\b(you had one job)\b.*',
        r'.*\b(they\'re the same picture)\b.*',
        r'.*\b(wait, that\'s illegal)\b.*',
        r'.*\b(i see this as an absolute win)\b.*',
        r'.*\b(i\'m something of a)\b.*',
        r'.*\b(myself)\b.*',
        r'.*\b(we don\'t do that here)\b.*',
        r'.*\b(i missed the part where that\'s my problem)\b.*',
        r'.*\b(i\'m gonna tell my kids)\b.*',
        r'.*\b(you know, i\'m something of a)\b.*',
        r'.*\b(i see no god up here)\b.*',
        r'.*\b(other than me)\b.*',
        r'.*\b(you wouldn\'t get it)\b.*',
        r'.*\b(i\'ve won, but at what cost)\b.*',
        r'.*\b(perhaps)\b.*',
        r'.*\b(visible confusion)\b.*',
        r'.*\b(understandable, have a nice day)\b.*',
        r'.*\b(i\'ll allow it)\b.*',
        r'.*\b(i\'ll fucking do it again)\b.*',
        r'.*\b(i know more than you)\b.*',
        r'.*\b(i\'m in danger)\b.*',
        r'.*\b(i\'m never gonna financially recover from this)\b.*',
        r'.*\b(i\'m once again asking)\b.*',
        r'.*\b(i\'m somewhat of a)\b.*',
        r'.*\b(i\'ve seen enough, i\'m satisfied)\b.*',
        r'.*\b(it\'s a trap)\b.*',
        r'.*\b(it\'s free real estate)\b.*',
        r'.*\b(just do it)\b.*',
        r'.*\b(listen here you little)\b.*',
        r'.*\b(modern problems require modern solutions)\b.*',
        r'.*\b(my disappointment is immeasurable)\b.*',
        r'.*\b(my day is ruined)\b.*',
        r'.*\b(no, i don\'t think i will)\b.*',
        r'.*\b(not bad kid)\b.*',
        r'.*\b(now this looks like a job for me)\b.*',
        r'.*\b(oh yeah, it\'s all coming together)\b.*',
        r'.*\b(parkour)\b.*',
        r'.*\b(perfectly balanced)\b.*',
        r'.*\b(as all things should be)\b.*',
        r'.*\b(professionals have standards)\b.*',
        r'.*\b(say sike right now)\b.*',
        r'.*\b(shut up and take my money)\b.*',
        r'.*\b(so anyway, i started blasting)\b.*',
        r'.*\b(so you have chosen death)\b.*',
        r'.*\b(stonks)\b.*',
        r'.*\b(that\'s what heroes do)\b.*',
        r'.*\b(that\'s where the trouble began)\b.*',
        r'.*\b(that smile)\b.*',
        r'.*\b(the sacred texts)\b.*',
        r'.*\b(the what)\b.*',
        r'.*\b(they had us in the first half)\b.*',
        r'.*\b(not gonna lie)\b.*',
        r'.*\b(this is fine)\b.*',
        r'.*\b(this is where the fun begins)\b.*',
        r'.*\b(thomas had never seen such bullshit before)\b.*',
        r'.*\b(wait, that\'s illegal)\b.*',
        r'.*\b(we don\'t do that here)\b.*',
        r'.*\b(well yes, but actually no)\b.*',
        r'.*\b(what the hell happened here)\b.*',
        r'.*\b(who are you, who are so wise in the ways of science)\b.*',
        r'.*\b(why would you say something so controversial yet so brave)\b.*',
        r'.*\b(you get what you fucking deserve)\b.*',
        r'.*\b(you know the rules and so do i)\b.*',
        r'.*\b(you wouldn\'t get it)\b.*',
        r'.*\b(you\'re goddamn right)\b.*',
    ]

    # Check if the meme name matches any of the patterns
    name_lower = name.lower()
    for pattern in text_response_patterns:
        if re.match(pattern, name_lower):
            return True

    # Additional heuristics for text response memes
    # Text response memes often contain certain phrases or structures
    if any(phrase in name_lower for phrase in [
        'when', 'that moment', 'me when', 'nobody:', 'no one:', 'be like',
        'how it feels', 'my face when', 'mfw', 'tfw', 'mrw', 'when you',
        'when they', 'when he', 'when she', 'when i', 'when we'
    ]):
        return True

    # Check if the meme is related to AI technologies
    if is_ai_related_meme(name):
        return True

    return False

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
