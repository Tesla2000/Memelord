import json
from collections.abc import Iterable

from litellm import completion
from pydantic import BaseModel, Field

def create_utterances(meme_titles: Iterable[str], meme_url: str) -> list[str]:
    return json.loads(
        completion(
            "gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"What is on this image {meme_url}?",
                }
            ],
            temperature=0.0,
            # response_format=_Utterances,
        ).choices[0]["message"]["content"]
    )

class _Utterances(BaseModel):
    utterances: list[str] = Field(description="Utterances that the message could respond to", default_factory=list)
