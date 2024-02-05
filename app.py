import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

st.set_page_config(page_title="YouTube Transcript Viewer", layout="wide")

# Custom CSS for styling
# Attempting to target labels more specifically with CSS
st.markdown(
    """
    <style>
    /* Background color for the app */
    .stApp { background-color: #f0f2f6; }

    /* Styling headings and descriptions to purple */
    h1, .stMarkdown, label, .stSelectbox label { color: #800080; }

    /* Text input styling - white background with purple text */
    .stTextInput>div>div>input { background-color: #fff; color: #800080; border-radius: 20px; border: 1px solid #800080; }

    /* Button styling - enhanced visibility */
    .stButton>button { margin: 2px; border: 2px solid #4CAF50; border-radius: 20px; color: #fff; background-color: #4CAF50; }

    /* Selectbox styling */
    .stSelectbox>div>div>select, .stSelectbox>div>label { color: #800080; } /* Purple text for dropdown and its label */

    /* Adjusting the width of the URL input to make it 100% wide */
    .stTextInput>div>div>input { width: 100%; }

    /* Text area styling */
    .stTextArea>div>div>textarea { color: #000; } /* Ensuring text area content is visible */
    </style>
    """,
    unsafe_allow_html=True
)



# Function to get available languages
def get_available_languages(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = [(transcript.language_code, transcript.language) for transcript in transcript_list]
        return languages
    except (TranscriptsDisabled, NoTranscriptFound):
        return []

# Function to get the transcript
def get_transcript(video_id, language_code):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)
        return transcript_text
    except Exception as e:
        return f"An error occurred: {e}"

# UI Elements for the Streamlit app
st.title('YouTube Video Transcript Viewer 📝', anchor=None)
st.markdown("Enter the URL of a YouTube video to fetch its transcript. Then, select the transcript's language.")

# URL input - now taking the full width of the app
video_url = st.text_input('YouTube Video URL:', '', placeholder="Paste YouTube video link here")

if video_url:
    video_id = video_url.split("v=")[1].split("&")[0]
    
    languages = get_available_languages(video_id)
    if languages:
        options = {code: lang for code, lang in languages}
        selected_lang = st.selectbox('Transcript Language:', options.keys(), format_func=lambda x: options[x])
        
        transcript = get_transcript(video_id, selected_lang)
        st.text_area("Transcript", value=transcript, height=300, disabled=True)

     # Add a copy to clipboard button
        st.download_button(label="Download Transcript", 
                           data=transcript, 
                           file_name="transcript.txt", 
                           mime="text/plain",
                           key="copy-transcript")
    else:
        st.error("Transcript not available or disabled for this video.")
