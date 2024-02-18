from typing import List
from fastapi import APIRouter
from app.api.youtube.logic import return_video_previews
from app.api.trends.logic import get_trending_topics
from app.api.processing.logic import process_videos

from app.schemas import VideoUrls
from app.schemas import Video

router = APIRouter()

@router.get("/trending", response_model=List[str])
async def trending_topics():
    return await get_trending_topics()

@router.post("/videos_preview")
async def videos_preview(video: Video):
    return await return_video_previews(video)

@router.post("/process_videos")
async def api_process_videos(video_urls: VideoUrls):
    return await process_videos(video_urls)
