import os
import time
import logging
import threading
from fastapi import HTTPException
from app.schemas import VideoUrls
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import google.generativeai as genai

from langchain.chains import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .utils import extract_video_id, DirectoryGenerator, renderBlog, parse_json_like_string, generate_deployment_url
from .templates import summarize_prompt, blog_gen_prompt


logger = logging.getLogger(__name__)

load_dotenv()

AZURE_API_KEY = os.getenv('AZURE_API_KEY128')
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT128')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
google_llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-pro")

llm = AzureChatOpenAI(api_key=AZURE_API_KEY, model="gpt-4",
                      openai_api_version="2023-07-01-preview", 
                      azure_endpoint=AZURE_ENDPOINT, temperature=0.55)

output_parser = StrOutputParser()


def fetch_and_summarize_transcript(url: str, result_container, index):
    try:
        start_thread_time = time.time()
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        summarize_chain = summarize_prompt | google_llm | output_parser
        result_container[index] = summarize_chain.invoke({"transcript": transcript})
        end_thread_time = time.time()
        print("=============================")
        print(f"Time for the thread {index} is {end_thread_time - start_thread_time}")
        print("=============================")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


def fetch_and_summarize_transcript_chunking(url: str, result_container, index):
    try:
        start_thread_time = time.time()
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        splitted_transcripts = []
        transcript_splitter = RecursiveCharacterTextSplitter(chunk_size=32000, chunk_overlap=3200)
        doc = [Document(page_content=str(transcript), metadata={"source": "local"})]
        splitted_transcripts.extend(transcript_splitter.split_documents(doc))
        summarize_chain = load_summarize_chain(llm=google_llm, chain_type="map_reduce")
        result_container[index] = summarize_chain.run({'input_documents': splitted_transcripts})
        end_thread_time = time.time()
        print("=============================")
        print(f"time for the thread {index} is {end_thread_time - start_thread_time}")
        print("=============================")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


async def generate_final_article(combined_summarized_transcript: str) -> dict:
    blog_gen_chain = blog_gen_prompt | llm | output_parser
    try:
        response = blog_gen_chain.invoke({'combined_summarized_transcript': combined_summarized_transcript})
        return response
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    

async def process_videos(video_urls: VideoUrls):
    try:
        start_time = time.time()
        print("Processing Started")
        combined_summarized_transcript = ""
        print("Checkpoint 1")
        results = [None for _ in range(len(video_urls.urls))]
        start_time_thread = time.time()
        threads = []
        for i, url in enumerate(video_urls.urls):
            thread = threading.Thread(target=fetch_and_summarize_transcript, args=(url, results, i))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        for transcript in results:
            combined_summarized_transcript += transcript + "\n\n\n\n"
        print("Checkpoint 2")
        json_output = await generate_final_article(combined_summarized_transcript)
        print("Checkpoint 3")
        json_output = parse_json_like_string(json_output)
        print("Checkpoint 4")
        html_content = renderBlog(title= json_output["Title"], question= json_output["Question"], author= json_output["Author"], paragraphs = json_output["Paragraphs"])
        print("Checkpoint 5")
        directory_name = DirectoryGenerator(html_content, "app/user")
        deployment_url = generate_deployment_url(directory_name)
        print(f"Processing Finished in {time.time() - start_time} seconds")
        return {"message": "The Processing Is Finished!", "deployment_url": deployment_url}
    except Exception as e:
        logger.error(f"An error occurred nnnnn: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during video processing.")
