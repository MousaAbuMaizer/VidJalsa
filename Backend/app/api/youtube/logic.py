from googleapiclient.discovery import build
<<<<<<< HEAD
import os 
=======
import os
>>>>>>> 33818dc86ccea265c36992c47e776e3d709f405b
from isodate import parse_duration
from fastapi import HTTPException
from app.schemas import Video
from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD
=======

>>>>>>> 33818dc86ccea265c36992c47e776e3d709f405b
def initialize_youtube_service() -> object:
    """Initialize and return the YouTube service."""
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        raise ValueError("YouTube API key not found in environment variables.")
    return build('youtube', 'v3', developerKey=api_key)


def fetch_search_results(youtube, topic: str, max_results: int) -> list:
    """Fetch search results from YouTube."""
    return youtube.search().list(
        q=topic,
        part='snippet',
        type='video',
        order='relevance',
        maxResults=max_results,
        safeSearch='strict',
<<<<<<< HEAD
        relevanceLanguage='en'
=======
        relevanceLanguage='en',
        videoCaption='closedCaption'
>>>>>>> 33818dc86ccea265c36992c47e776e3d709f405b
    ).execute()


def extract_video_ids(search_response: dict) -> list:
    """Extract video IDs from search results."""
    return [item['id']['videoId'] for item in search_response['items']]


def fetch_video_details(youtube, video_ids: list) -> dict:
    """Fetch details for a list of video IDs."""
    response = youtube.videos().list(part="contentDetails", id=",".join(video_ids)).execute()
<<<<<<< HEAD
    return {item['id']: parse_duration(item['contentDetails']['duration']).total_seconds() for item in response['items']}
=======
    return {item['id']: parse_duration(item['contentDetails']['duration']).total_seconds() for item in
            response['items']}
>>>>>>> 33818dc86ccea265c36992c47e776e3d709f405b


def filter_videos(video_ids: list, video_details_map: dict, search_response: dict, max_results: int) -> list:
    """Filter videos based on criteria and format the response."""
    videos_info = []
    for video_id in video_ids:
        if video_id not in video_details_map or len(videos_info) >= max_results:
            continue
        duration_seconds = video_details_map[video_id]
        if not (60 < duration_seconds < 1800):
            continue
        for item in search_response['items']:
            if item['id']['videoId'] == video_id:
                videos_info.append(format_video_info(item))
                break
    return videos_info


def format_video_info(video_item: dict) -> dict:
    """Format video information for the response."""
    return {
        'title': video_item['snippet']['title'],
        'link': f"https://www.youtube.com/watch?v={video_item['id']['videoId']}",
        'thumbnail': video_item['snippet']['thumbnails']['high']['url'],
        'video_id': video_item['id']['videoId'],
    }


<<<<<<< HEAD
async def return_video_previews(video: Video) :
=======
async def return_video_previews(video: Video):
>>>>>>> 33818dc86ccea265c36992c47e776e3d709f405b
    """Return a list of video previews based on the video topic."""
    try:
        youtube = initialize_youtube_service()
        search_response = fetch_search_results(youtube, video.video.lower(), 30)
        video_ids = extract_video_ids(search_response)
        video_details_map = fetch_video_details(youtube, video_ids)
        videos_info = filter_videos(video_ids, video_details_map, search_response, 30)
        return videos_info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
<<<<<<< HEAD
        raise HTTPException(status_code=500, detail="Failed to fetch video previews.")    
=======
        raise HTTPException(status_code=500, detail="Failed to fetch video previews.")
>>>>>>> 33818dc86ccea265c36992c47e776e3d709f405b
