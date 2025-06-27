import streamlit as st

# Page configuration
st.set_page_config(page_title="Main Page", page_icon="🏠", layout="wide")

# Title and Subtitle
st.title("🎬 Audio & Video Summarizer")
st.subheader("Transform your media into meaningful insights!")

st.write("Select an option to proceed:")

# Layout with images
col1, col2, col3 = st.columns(3)

with col1:
    st.image("assets/video.webp", width=200)  # Replace with actual image path
    if st.button("📺 YouTube Summary"):
        st.switch_page("pages/youtube.py")

with col2:
    st.image("assets/audio.webp", width=200)  # Replace with actual image path
    if st.button("🎤 Audio Summary"):
        st.switch_page("pages/audio and video.py")

with col3:
    st.image("assets/bot.webp", width=200)  # Replace with actual image path
    if st.button("🤖 AI Chatbot"):
        st.switch_page("pages/chatbot.py")

# Blog Section: Use Cases of Audio & Video Summarization
st.markdown("---")
st.header("📖 Blog: Use Cases of Audio & Video Summarization")
st.image("assets/diagram.webp", width=700)  # Replace with actual image path

st.write("""
In today's fast-paced world, **audio and video summarization** is revolutionizing how we consume media. 
Here are some key use cases:

### 🎓 **Education & E-Learning**  
- Quickly summarize **lecture recordings** for students.  
- Convert lengthy educational videos into **concise text summaries**.  
- Help non-native speakers understand **key topics** in a shorter time.  

### 🏢 **Business & Meetings**  
- Convert **meeting recordings** into readable text for easy reference.  
- Summarize lengthy **podcasts & interviews** into actionable insights.  
- Automate **note-taking** for professionals and researchers.  

### 📺 **Media & Entertainment**  
- Generate **instant movie & documentary summaries**.  
- Create subtitles and closed captions for **enhanced accessibility**.  
- Summarize news reports for **quick insights**.  

### 📢 **Marketing & Content Creation**  
- Transform **customer feedback** from calls and videos into reports.  
- Summarize **video ads** for market analysis.  
- Help content creators repurpose **long-form content into social media snippets**.  

With AI-powered summarization, accessing key insights from audio and video has never been easier! 🚀  
""")

# Footer
st.markdown("---")
st.markdown("🔗 *Developed with ❤️ using Streamlit*")
