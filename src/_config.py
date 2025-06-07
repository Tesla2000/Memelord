from pathlib import Path
from typing import Any

from config_parser import ConfigBase
from pydantic import Field


class Config(ConfigBase):
    message: str = Field(description="Message meme responses should be created for")
    re_fetch: bool = False
    meme_folder: Path = Field(default_factory=lambda: Path("memes"), description='Whether to re-pull memes from')
    classified_memes_file: Path = Field(default_factory=lambda: Path("classified_memes.txt"), description='File for storing classified meme files')
    n_results: int = Field(default=5, description='N most fitting memes', ge=1)
    distillation_factor: float = Field(default=.1, description='What fraction of memes should remain after each pass', gt=0, lt=1)
    include_non_response: bool = Field(default=False, description="Wherethere to include meme template classified as non response")
    initial_model: str = Field(default="gpt-4o-mini", description="Model used to distill memes on the first passes. Less specific")
    final_model: str = Field(default="gpt-4o", description="Model used to distill memes on the second and later passes. More specific")
    initial_model_passes: int = Field(default=1, description="Number of passes initial model should be involved in", ge=0)


    def __init__(self, /, **data: Any):
        data["message"] = data.get("message") or (data.get("pos_args") or [None])[0] or input("Write a message for which to create responses: ")
        super().__init__(**data)