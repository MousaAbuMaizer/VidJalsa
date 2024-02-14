# VidJalsa: Automated Blog Generator

## Introduction
VidJalsa is an innovative platform that revolutionizes content creation by automating the generation of blog posts from YouTube videos. Leveraging the cutting-edge capabilities of Azure's GPT-4, VidJalsa provides a seamless experience from video to narrative, transforming multimedia content into engaging articles.

## Features
- **Automated Blog Posts:** Create blog content automatically from YouTube video transcripts.
- **Powered by GPT-4:** Utilize the advanced natural language processing capabilities of Azure's GPT-4 for high-quality writing.
- **React Frontend:** A sleek and modern user interface built with React.js for an intuitive user experience.

## Technology Stack
- **Frontend:** React.js
- **Backend:** Python FastAPI
- **APIs:** YouTube Data API, Azure OpenAI Service

## Installation
To set up VidJalsa for local development or deployment, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/MousaAbuMaizer/VidJalsa.git
   ```
2. Navigate to the project directory:
   ```
   cd VidJalsa
   ```
3. Install dependencies for the backend:
   ```
   pip install -r Backend/requirements.txt
   ```
4. Install dependencies for the frontend:
   ```
   cd FrontEnd
   npm install
   ```
5. Set up environment variables in `.env` file with your Azure and YouTube API keys.

## Usage
To run VidJalsa locally:

1. Start the backend server:
   ```
   uvicorn app:app --reload --port 7000
   ```
2. Start the frontend application:
   ```
   npm start
   ```
   This will launch the React app in your default browser.

3. To generate a blog post, pick a topic, choose the videos based on the topic, and then press 'Create'.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact
For support or any queries, please reach out to [contact information].