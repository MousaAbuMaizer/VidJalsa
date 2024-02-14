from fastapi import FastAPI
from pytrends.request import TrendReq
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from googleapiclient.discovery import build
from isodate import parse_duration
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from typing import List, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
import os
import json
from renderBlog import renderBlog
import uuid
from fastapi.staticfiles import StaticFiles
from googleapiclient.discovery import build


app = FastAPI()

deployment_directory_folder = "users_output"
app.mount("/" + deployment_directory_folder, StaticFiles(directory=deployment_directory_folder), name=deployment_directory_folder)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

load_dotenv()

#+-----------------------------------+
#|       Trending Topics API         |
#+-----------------------------------+
@app.get("/api/trending", response_model=List[str])
async def get_trending_topics():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending = pytrends.trending_searches(pn='united_states')
    topics = trending[0].head(8).tolist()  
    return topics

#+-----------------------------------+
#|        Youtube Videos API         |
#+-----------------------------------+
class Video(BaseModel):
    video: str

@app.post("/api/videos_preview")
async def return_video(video: Video):
    try:
        topic = video.video.lower()  
        maxResults = 8
        videos_info = []
        pageToken = None
        api_key = "AIzaSyCSIYVJRr6Gyid80eEdhyiZwS17TnWcFb0"
        youtube = build('youtube', 'v3', developerKey=api_key)
        while len(videos_info) < maxResults:
            search = youtube.search().list(
                q=topic,
                part='snippet',
                type='video',
                order='relevance',
                maxResults=maxResults,
                pageToken=pageToken,
                safeSearch='strict',  
                relevanceLanguage='en'  
            ).execute()
            for item in search['items']:
                video_id = item['id']['videoId']

                transcript_available = True
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    if len(transcript) > 32000:
                        continue
                except Exception as e:
                    transcript_available = False
                
                if not transcript_available:
                    continue

                video_title = item['snippet']['title']
                video_link = 'https://www.youtube.com/watch?v=' + video_id
                thumbnail = item['snippet']['thumbnails']['high']['url']
                
                # if topic.lower() not in video_title.lower():
                #     continue
                
                video_details = youtube.videos().list(part="contentDetails", id=video_id).execute()
                duration = parse_duration(video_details['items'][0]['contentDetails']['duration'])
                
                if not (60 < duration.total_seconds() < 900):  
                    continue
                
                video_info = {
                    'title': video_title,
                    'link': video_link,
                    'thumbnail': thumbnail,
                    'video_id': video_id,
                }
                videos_info.append(video_info)
                
                if len(videos_info) == maxResults:
                    break
            
            pageToken = search.get('nextPageToken')
            if not pageToken:
                break
        
        return videos_info
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

#+-----------------------------------+
#|         Main Process API          |
#+-----------------------------------+
def parse_article(content):
    pattern = r'\*\*(.+?)\*\*:\s*"(.+?)"'
    matches = re.findall(pattern, content, re.DOTALL)

    article_json = {'Paragraphs': []}
    for key, value in matches:
        if "Paragraph" in key:
            article_json['Paragraphs'].append(value)
        else:
            article_json[key] = value

    return article_json

def DirectoryGenerator(html_content , deployment_directory):

    user_id = str(uuid.uuid4())
    user_output_dir = os.path.join(deployment_directory, user_id)
    os.makedirs(user_output_dir, exist_ok=True)

    with open(os.path.join(user_output_dir, "index.html"), "w") as html_file:
        html_file.write(html_content)

    return user_output_dir


def extract_video_id(url: str) -> str:
    regex_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\s]+)',
        r'(?:https?:\/\/)?youtu\.be\/([^&\s]+)',  
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^&\s]+)', 
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^&\s]+)'
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""

class VideoUrls(BaseModel):
    urls: List[str]

@app.post("/api/process_videos")
async def process_videos(video_urls: VideoUrls):
    
    prompt1 = PromptTemplate.from_template("""
    **Enhanced Summarization Task for Web Content Creation**

    You are provided with a transcript collection: `{transcript}`. Your mission is to distill this material into a seamless, engaging narrative suitable for a web page audience. This task requires a blend of precision, creativity, and adherence to the following enhanced guidelines:

    1. **Unified Core Summarization:**  
    Craft a cohesive summary that seamlessly integrates the main themes, critical points, and significant details from the transcript. Aim for a narrative that flows logically, avoiding disjointed sections or headings. The essence and informational richness of the original material should be preserved in a narrative that reads smoothly from start to finish.

    2. **Narrative Enrichment:**  
    Where the transcript is lacking in detail or context, enrich the narrative with relevant additional information that provides value and depth. Ensure these enhancements complement the core material, contributing to a well-rounded and comprehensive understanding of the subject without diluting the original message.

    3. **Focused Relevance:**  
    Maintain strict relevance to the subject matter of transcript. Exclude any extraneous or off-topic content to ensure the narrative remains focused and integrity is preserved. Every sentence should contribute to a deeper understanding or appreciation of the topic at hand.

    4. **Audience-Centric Appropriateness:**  
    Tailor your summary to the broad spectrum of web users, ensuring the content is universally accessible, respectful, and devoid of any material that could be considered inappropriate or offensive. The narrative should be welcoming to all readers, fostering an inclusive and informative environment.

    5. **Verbal Content Emphasis:**  
    Given the unique challenges of translating video transcripts to text, omit non-verbal elements and focus solely on the verbal content's informational essence. This approach ensures the narrative remains clear and accessible without the need for visual or auditory cues.

    6. **Inclusivity of Essential Insights:**  
    Guarantee that all pivotal insights, arguments, and data from the transcript are woven into the narrative. This inclusive approach ensures the reader gains a full and accurate understanding of the topic without needing to refer to the original video content.

    7. **Diligent Content Review:**  
    Upon concluding your summarization, meticulously review the narrative for coherence, completeness, and alignment with these guidelines. The final piece should stand as a testament to quality, engaging and informing readers without necessitating prior knowledge of the original transcripts.

    By diligently applying these refined guidelines, you will create a narrative that not only captivates and informs but also meets the high standards required for web page content. We appreciate your commitment to crafting content that resonates with readers and elevates their online experience.

    """)  
    
    prompt2 = PromptTemplate.from_template("""
    **Task: Generate a Medium-Style Article as a JSON Object**

    **Objective:** Create a captivating article based on the summarized content provided in `{combined_summarized_transcript}`. The article must reflect the style of Medium publications, which are recognized for their engaging titles, thought-provoking questions, distinctive authorship, and coherent narrative flow. The output should be a JSON object that includes these elements derived from the given input.

    **Process Overview:**

    - **Input:** A single variable, `{combined_summarized_transcript}`, which contains summarized text on a contemporary topic.
    - **Output:** A JSON object structured with four key components: Title, Question, Author, and Paragraphs.

    **Detailed Instructions for JSON Structure:**

    1. **Title:** Generate a compelling title that captures the essence of the summarized text. The title must be eye-catching and reflective of the content’s core message.

    2. **Question:** Craft a thought-provoking question pertinent to the article's theme. This question should spark curiosity and motivate the reader to explore the topic further.

    3. **Author:** Invent an author name that incorporates "AI" in uppercase, indicating the AI-enhanced creation of the article. Ensure that this name is plausible and fits within the context of authorship on Medium. Ensure also that they are real names for humans and contain a first and last name.

    4. **Paragraphs:** Divide the `{combined_summarized_transcript}` into an array of paragraphs. Each paragraph should encapsulate a distinct idea or aspect of the summary, maintaining a logical flow and engaging the reader with a tone that is both conversational and accessible.

    **Output Formatting Requirement:**

    The output must be formatted as a JSON object as follows:

    ```json
    {{
        "Title": "Generated Title Based on Summary",
        "Question": "Generated Question Based on Summary",
        "Author": "Generated Author Name Including AI",
        "Paragraphs": [
            "First paragraph of the article...",
            "Second paragraph of the article...",
            "...additional paragraphs as derived from the summarized text"
        ]
    }}
    ```

    The content generation process should be strictly based on the input summary, without requiring any additional inputs. The JSON structure is designed to organize the content neatly, facilitating its direct application or web deployment.

    """)

    azure_api_key = os.getenv('AZURE_API_KEY')
    azure_endpoint = os.getenv('AZURE_ENDPOINT')

    llm = AzureChatOpenAI(api_key= azure_api_key, model="gpt-4-32K",openai_api_version="2023-07-01-preview",azure_endpoint = azure_endpoint,temperature=0.55)

    combined_summarized_transcript = ""
    
    print("Received video URLs:", video_urls.urls)

    for url in video_urls.urls:
        video_id = extract_video_id(url)          
        data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in data])
          
        output_parser = StrOutputParser()
        chain = prompt1 | llm | output_parser
        
        summarized_transcript = chain.invoke({"transcript": transcript})
        
        combined_summarized_transcript += summarized_transcript + "\n\n\n\n"
        print("Checkpoint 1")
        
    chain2 = prompt2 | llm | output_parser 
    response = chain2.invoke({'combined_summarized_transcript': combined_summarized_transcript})

    # Save the output as a text file
    output_path = "/Users/mabumaizer001/PwC Projects/video-scriptum/Backend/summarized_trans.txt"
    with open(output_path, 'w') as file:
        file.write(response)

    print("Checkpoint 2")
    json_output = json.loads(response)
    
    title = json_output["Title"]
    question = json_output["Question"]
    author = json_output["Author"]
    paragraphs = json_output["Paragraphs"]

    html_content = renderBlog(title, question, author, paragraphs)
    
    directory_name = DirectoryGenerator(html_content , deployment_directory_folder)

    deployment_url = f"http://127.0.0.1:7000/{directory_name}/index.html"
        
    return {"message": "The Processing Is Finished!", "deployment_url": deployment_url}
