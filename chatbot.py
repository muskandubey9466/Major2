import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

# Function to get response from Gemini
def get_gemini_response(prompt):
    response = chat.send_message(prompt, stream=True)
    return "".join(chunk.text for chunk in response)

# Streamlit app configuration
st.set_page_config(page_title="SAVA Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 SAVA: AI Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(f"**{role.capitalize()}:** {text}")

# User input
if prompt := st.chat_input("Ask something..."):
    # Display user's message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append(("user", prompt))

    # Generate and display AI response
    with st.spinner("Thinking..."):
        ai_response = get_gemini_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.chat_history.append(("assistant", ai_response))
