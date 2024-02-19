from pydantic import BaseModel
from typing import List

class Video(BaseModel):
    video: str  

class VideoUrls(BaseModel):
    urls: List[str]