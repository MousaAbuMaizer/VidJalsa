import os
import json
import threading
import time
import logging
from fastapi import HTTPException
from langchain.chains import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader

from .utils import extract_video_id, DirectoryGenerator, renderBlog , parse_json_like_string
from app.schemas import VideoUrls
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.docstore.document import Document

from dotenv import load_dotenv


from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
google_llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-pro")


load_dotenv()

logger = logging.getLogger(__name__)

AZURE_API_KEY = os.getenv('AZURE_API_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
DEPLOYMENT_DIRECTORY = "path/to/deployment/directory"

llm = AzureChatOpenAI(api_key=AZURE_API_KEY, model="gpt-4",
                             openai_api_version="2023-07-01-preview", 
                             azure_endpoint=AZURE_ENDPOINT, temperature=0.55)

output_parser = StrOutputParser()

def fetch_and_summarize_transcript(url: str , result_container, index) :
    start_thread_time = time.time()
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
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
    chain = prompt1 | google_llm | output_parser
    result_container[index] = chain.invoke({"transcript": transcript})
    end_thread_time = time.time()
    print("=============================")
    print(f"the url is being tested is {url}" )
    print(f"time for the thread {index} is {end_thread_time - start_thread_time}" )
    print("=============================")



async def generate_final_article(combined_summarized_transcript: str) -> dict:
    print("Checkpoint 2-A")


    prompt2 = PromptTemplate.from_template("""
    **Task: Generate a Medium-Style Article as a JSON Object**

    **Objective:** Create a captivating article based on the summarized content provided provided as follows: 
    {combined_summarized_transcript}
    
    The article must reflect the style of Medium publications, which are recognized for their engaging titles, thought-provoking questions, distinctive authorship, and coherent narrative flow. The output should be a JSON object that includes these elements derived from the given input.

    **Process Overview:**

    - **Input:** A single variable, combined summarized transcript, which contains summarized text on a contemporary topic.
    - **Output:** A JSON object structured with four key components: Title, Question, Author, and Paragraphs.

    **Detailed Instructions for JSON Structure:**

    1. **Title:** Generate a compelling title that captures the essence of the summarized text. The title must be eye-catching and reflective of the content’s core message.

    2. **Question:** Craft a thought-provoking question pertinent to the article's theme. This question should spark curiosity and motivate the reader to explore the topic further.

    3. **Author:** Invent an author name that incorporates "AI" in uppercase, indicating the AI-enhanced creation of the article. Ensure that this name is plausible and fits within the context of authorship on Medium. Ensure also that they are real names for humans and contain a first and last name.

    4. **Paragraphs:** Divide the combined summarized transcripts into an array of paragraphs. Each paragraph should encapsulate a distinct idea or aspect of the summary, maintaining a logical flow and engaging the reader with a tone that is both conversational and accessible.

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

    """
     )
    final_chain = prompt2 | llm | output_parser
    
    print("Checkpoint 2-B")

    try:
        response = final_chain.invoke({'combined_summarized_transcript': combined_summarized_transcript})
        print("Checkpoint 2-C", response)
        return response
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    

def generate_deployment_url(directory_name: str) -> str:
    return f"http://127.0.0.1:7000/{directory_name}/index.html"

async def process_videos(video_urls: VideoUrls):
    start_time = time.time()
    print("Processing Started")

    combined_summarized_transcript = ""
    
    print("Checkpoint 1")
    
    try:

        results = [None for _ in range(len(video_urls.urls))]
        start_time_thread = time.time()
        threads = []
        for i, url in enumerate(video_urls.urls):
            thread = threading.Thread(target=fetch_and_summarize_transcript2, args=(url, results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        end_time_thread = time.time()

        print(f"hamza total time {end_time_thread - start_time_thread} ")

        for transcript in results:
            combined_summarized_transcript += transcript + "\n\n\n\n"

        print("Checkpoint 2")
        print(f"generate_final_article input is {combined_summarized_transcript}" )
        json_output = await generate_final_article(combined_summarized_transcript)
        print(json_output)
        print("Checkpoint 3")
        json_output = parse_json_like_string(json_output)
        title = json_output["Title"]
        question = json_output["Question"]
        author = json_output["Author"]
        paragraphs = json_output["Paragraphs"]

        print("Checkpoint 4")

        html_content = renderBlog(title, question, author, paragraphs)

        print("Checkpoint 5")

        directory_name = DirectoryGenerator(html_content, "app/user")
        deployment_url = generate_deployment_url(directory_name)

        print(f"Processing Finished in {time.time() - start_time} seconds")
        return {"message": "The Processing Is Finished!", "deployment_url": deployment_url}

    except Exception as e:
        logger.error(f"An error occurred nnnnn: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during video processing.")



def fetch_and_summarize_transcript2(url: str, result_container, index):
    start_thread_time = time.time()


    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)


    splited_transcripts = []
    transcript_spliter = RecursiveCharacterTextSplitter(chunk_size=32000, chunk_overlap=3200)
    doc = [Document(page_content=str(transcript), metadata={"source": "local"})]
    splited_transcripts.extend(transcript_spliter.split_documents(doc))
    print(f"  hamza_splited_transcripts {splited_transcripts}")
    print(f"  hamza_splited_transcripts_len {len(splited_transcripts)}")

    summarize_chain = load_summarize_chain(llm=google_llm, chain_type="map_reduce")
    result_container[index] = summarize_chain.run({'input_documents': splited_transcripts})
    end_thread_time = time.time()
    print("=============================")
    print(f"the url is being tested is {url}")
    print(f"time for the thread {index} is {end_thread_time - start_thread_time}")
    print("=============================")