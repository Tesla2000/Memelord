"""
Script to select an appropriate meme from an iterable of MemeImage objects
based on meme names rather than conversation context.
"""
import json
import os
from itertools import count, takewhile
from pathlib import Path

from pydantic import Field
from typing import Iterable, List, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel

from meme_scraper import MemeImage

# Load environment variables from .env file
load_dotenv()


class MemeUses(BaseModel):
    requests: list[str] = Field(description="""Not more than 5 short messages it can respond to. 
If the meme can't be easily used as a response (is not a simple message and requires big modifications) for example Drake format return empty list.
Example:
    Title: I find your lack of faith disturbing
    Requests: ['You won't believe', 'No way you can handle this', 'I'm atheist']
Example:
    Title: Drake Format
    Requests: []""")
    is_title_response: bool = Field(description="Can you picture yourself in a situation in which you send this meme without modification to someone as a response to his message?"
                                    )
    contains_verb: bool = Field(description="Does the title contain a verb. Make sure that verb is not a noun based on other words in the title")
    contains_verb_explanation: str

def filter_memes(memes: Iterable[MemeImage]) -> dict[str, list[str]]:
    model = ChatOpenAI(temperature=.0, model="gpt-4o-mini").with_structured_output(MemeUses)
    valid_memes = {}
    for meme in memes:
        uses: MemeUses = model.invoke(
            f"Create {MemeUses.__name__} object. Title of the meme template\n{meme.title}'"
        )
        if not (uses.contains_verb and uses.is_title_response and uses.requests):
            continue
        valid_memes[meme.title] = uses.requests
    return valid_memes

def load_memes_from_file(file_path: str) -> List[MemeImage]:
    """
    Load MemeImage objects from a file.
    
    Args:
        file_path: Path to the file containing MemeImage objects
        
    Returns:
        List of MemeImage objects
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    memes = []
    for line in lines:
        # Parse the MemeImage from the string representation
        # Format: MemeImage(title='Title', url='URL', hash='HASH')
        line = line.strip()
        if not line:
            continue
            
        # Extract the parts using string manipulation
        parts = line.split("'")
        if len(parts) >= 6:
            title = parts[1]
            url = parts[3]
            hash_value = parts[5]
            memes.append(MemeImage(title=title, url=url, hash=hash_value))
    
    return memes

if __name__ == "__main__":
    for i in takewhile(lambda i: Path(f"memes/{i}.txt").exists(), count(1)):
        memes = load_memes_from_file(f"memes/{i}.txt")
        filtered_memes = filter_memes(memes)
        Path(f"filtered_memes/{i}.json").write_text(json.dumps(filtered_memes, indent=2))