import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Google API Key for YouTube Data API
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Define prompt for summarization
PROMPT = """You are a YouTube video summarizer. Given a video's content, generate a detailed summary. 
If a transcript is available, summarize it within 1000 words.
If no transcript is available, generate an insightful summary based on available information.
Provide key points in a clear format.
Here is the input: """

# Function to extract transcript
def extract_transcript(youtube_url):
    try:
        if "watch?v=" in youtube_url:
            video_id = youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
        else:
            return None, None, "Invalid YouTube URL format."

        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript_list])
        return video_id, transcript_text, None
    except Exception:
        return video_id, None, None  # Hide error messages from users

# Function to fetch video metadata
def get_video_metadata(video_id):
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        title = response["items"][0]["snippet"]["title"]
        return title
    except Exception:
        return None

# Function to generate summary
def generate_summary(input_text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(PROMPT + input_text)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Streamlit UI
st.title("🎥 YouTube Video Summarizer")

youtube_link = st.text_input("🔗 Enter YouTube Video Link:")

if youtube_link:
    try:
        if "watch?v=" in youtube_link:
            video_id = youtube_link.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_link:
            video_id = youtube_link.split("youtu.be/")[1].split("?")[0]
        else:
            st.error("⚠️ Invalid YouTube URL format. Please enter a valid video link.")
            video_id = None

        if video_id:
            st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except IndexError:
        st.error("⚠️ Invalid YouTube URL. Please enter a valid video link.")

if st.button("📄 Get Detailed Notes"):
    if not youtube_link:
        st.error("⚠️ Please enter a valid YouTube video link.")
    else:
        video_id, transcript_text, _ = extract_transcript(youtube_link)

        if transcript_text:
            summary = generate_summary(transcript_text)
        else:
            video_metadata = get_video_metadata(video_id)
            if video_metadata:
                summary = generate_summary(video_metadata)
            else:
                st.error("❌ Unable to retrieve video content. Try another video.")
                summary = None

        if summary:
            st.markdown("## 📌 Detailed Notes:")
            st.write(summary)
