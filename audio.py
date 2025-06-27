import os
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import ffmpeg
import google.generativeai as genai
from dotenv import load_dotenv
import tempfile

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return "".join(chunk.text for chunk in response)

def generate_summary(text):
    summary_prompt = f"Summarize the following text:\n{text}"
    return get_gemini_response(summary_prompt)

def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Could not request results, check internet connection."

# Function to extract audio from video using ffmpeg
def extract_audio_from_video(video_path, output_audio_path):
    try:
        ffmpeg.input(video_path).output(output_audio_path, format='wav').run(overwrite_output=True)
        return output_audio_path
    except Exception as e:
        return f"Error extracting audio: {str(e)}"

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page configuration
st.set_page_config(page_title="SAVA", page_icon="🤖", layout="wide")

# Header
st.title("🤖 Audio and Video Summarizer")

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(f"**{role.capitalize()}:** {text}")

# Create columns
col1, col2 = st.columns(2)

with col1:
    # Upload audio file
    uploaded_audio = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    if uploaded_audio is not None:
        audio_path = f"temp_audio.{uploaded_audio.name.split('.')[-1]}"
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())
        if uploaded_audio.name.endswith(".mp3"):
            sound = AudioSegment.from_mp3(audio_path)
            audio_path = "temp_audio.wav"
            sound.export(audio_path, format="wav")
        extracted_text = audio_to_text(audio_path)
        st.write("**Extracted Text from Audio:**", extracted_text)
        with st.spinner("Generating summary..."):
            audio_summary = generate_summary(extracted_text)
        st.write("**Summary of Audio Content:**", audio_summary)
        st.session_state.chat_history.append(("USER", extracted_text))
        st.session_state.chat_history.append(("assistant", audio_summary))
        os.remove(audio_path)

    # Upload video file
    uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    if uploaded_video is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_video.read())
            video_path = temp_video.name
        audio_path = "temp_audio.wav"
        extract_audio_from_video(video_path, audio_path)
        extracted_text = audio_to_text(audio_path)
        st.write("**Extracted Text from Video Audio:**", extracted_text)
        with st.spinner("Generating summary..."):
            video_summary = generate_summary(extracted_text)
        st.write("**Summary of Video Content:**", video_summary)
        st.session_state.chat_history.append(("USER", extracted_text))
        st.session_state.chat_history.append(("assistant", video_summary))
        os.remove(video_path)
        os.remove(audio_path)

# User text input
if prompt := st.chat_input("Enter your question here..."):
    with st.chat_message("user"):
        st.markdown(f"**You:** {prompt}")
    with st.spinner("Generating response..."):
        ai_response = get_gemini_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(f"**Bot:** {ai_response}")
    st.session_state.chat_history.append(("user", prompt))
    st.session_state.chat_history.append(("assistant", ai_response))
