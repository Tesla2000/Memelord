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
- Selects appropriate memes for conversation responses using AI

## Requirements

- Python 3.12 or higher
- requests
- beautifulsoup4
- Pillow
- langchain-core
- langchain-openai
- python-dotenv

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -e .
   ```

## Usage

### Scraping Memes

Run the scraper script:

```
python meme_scraper.py
```

This will:
1. Scrape meme templates from imgflip.com
2. Extract meme names and image URLs
3. Detect duplicate images
4. Filter memes that classify as "text response"
5. Save the filtered memes to `text_response_memes.json`

### Selecting Memes for Conversations

The `meme_selector.py` script provides functionality to select the most appropriate meme for a given conversation context:

```python
from meme_selector import select_meme, load_memes_from_file

# Load memes from a file
memes = load_memes_from_file("memes/1.txt")

# Example conversation
conversation = "I've been debugging this code for hours and still can't find the issue."

# Select the most appropriate meme
selected_meme = select_meme(memes, conversation)

# Use the selected meme
print(f"Selected meme: {selected_meme.title}")
print(f"URL: {selected_meme.url}")
```

### Selecting Memes Based on Names

Alternatively, you can use the `meme_picker.py` script to select memes based on their names rather than conversation context:

```python
from meme_filter import filter_memes, load_memes_from_file

# Load memes from a file
memes = load_memes_from_file("memes/1.txt")

# Select an appropriate meme based on meme names
selected_meme = filter_memes(memes)

# Use the selected meme
print(f"Selected meme: {selected_meme.title}")
print(f"URL: {selected_meme.url}")
```

Both scripts use OpenAI's API to select appropriate memes. Make sure to set your OpenAI API key in a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

You'll need to install the python-dotenv package to use the .env file:

```
pip install python-dotenv
```

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
