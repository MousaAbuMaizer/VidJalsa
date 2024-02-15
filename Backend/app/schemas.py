from pydantic import BaseModel
from typing import List

class Video(BaseModel):
    video: str  # and other fields as necessary

class VideoUrls(BaseModel):
    urls: List[str]