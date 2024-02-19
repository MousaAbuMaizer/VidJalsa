from langchain.prompts import PromptTemplate


summarize_prompt = PromptTemplate.from_template("""
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


blog_gen_prompt = PromptTemplate.from_template("""
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
""")