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
                    "content": "Given possible meme titles create a list of utterances that are message the meme could respond with little or without modifications."
                               "\nMEME TITLES:\n"
                               "\n".join(meme_titles),
                }
            ],
            temperature=0.0,
            response_format=_Utterances,
        ).choices[0]["message"]["content"]
    )["utterances"]

class _Utterances(BaseModel):
    utterances: list[str] = Field(description="Utterances that the message could respond to", default_factory=list)
