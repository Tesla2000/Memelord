# Memelord

A Python tool for scraping and classifying meme templates from imgflip.com.

## Description

This tool scrapes meme templates from imgflip.com, extracts their names and image URLs, detects duplicate images using hashing, and filters memes that classify as "text response" memes. The filtered memes are saved to a JSON file.

## Features

- Scrapes meme templates from imgflip.com
- Extracts meme names and image URLs
- Detects duplicate images using perceptual hashing
- Classifies memes as "text response" or not
- Saves filtered memes to a JSON file

## Requirements

- Python 3.12 or higher
- requests
- beautifulsoup4
- Pillow

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -e .
   ```

## Usage

Run the script:

```
python meme_scraper.py
```

This will:
1. Scrape meme templates from imgflip.com
2. Extract meme names and image URLs
3. Detect duplicate images
4. Filter memes that classify as "text response"
5. Save the filtered memes to `text_response_memes.json`

## Output

The script generates a JSON file (`text_response_memes.json`) with the following structure:

```json
{
  "Meme Name 1": "Image URL 1",
  "Meme Name 2": "Image URL 2",
  ...
}
```

## What are "Text Response" Memes?

Text response memes are memes that are typically used as reactions or responses in conversations. Examples include:
- "Always Has Been"
- "X, X Everywhere"
- "One Does Not Simply"
- "Change My Mind"

These memes usually contain text that can be used as a response to a situation or statement.

Additionally, memes related to AI technologies like LangChain, Pydantic, AI, or LiteLLM are also classified as text response memes. Examples include:
- "When LangChain fails to connect to the API"
- "Pydantic validation errors be like"
- "AI trying to understand human emotions"
- "LiteLLM: Am I a joke to you?"
