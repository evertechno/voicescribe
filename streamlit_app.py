import streamlit as st
import requests
import os
import time
from datetime import datetime

# Set up Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"

# Retrieve Hugging Face API token from Streamlit secrets
API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to send the audio file to the API
def transcribe_audio(file):
    try:
        # Read the file as binary
        data = file.read()
        response = requests.post(API_URL, headers=HEADERS, data=data)
        if response.status_code == 200:
            return response.json()  # Return transcription
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Additional helper function to log errors
def log_error(error_message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {error_message}\n")

# Streamlit UI
st.title("🎙️ Audio Transcription Web App")
st.write("Upload an audio file, and this app will transcribe it using OpenAI Whisper via Hugging Face API.")

# Feature 1: Support for multiple file types (audio file formats)
file_types = ["wav", "flac", "mp3", "m4a", "ogg", "webm", "aac"]
uploaded_file = st.file_uploader("Upload your audio file", type=file_types)

# Feature 2: Displaying file size and type info
if uploaded_file is not None:
    st.write(f"File name: {uploaded_file.name}")
    st.write(f"File type: {uploaded_file.type}")
    st.write(f"File size: {round(uploaded_file.size / 1024, 2)} KB")

# Feature 3: Show file upload progress bar
if uploaded_file is not None:
    st.progress(0.5)

# Feature 4: Add instructions for file upload
st.markdown("""
**Instructions:**
1. Choose an audio file (e.g., .mp3, .wav, .flac, etc.).
2. Wait for the transcription process to complete.
3. Download the transcribed text.
""")

# Feature 5: Audio duration info
if uploaded_file is not None:
    import pydub
    audio = pydub.AudioSegment.from_file(uploaded_file)
    duration = round(audio.duration_seconds, 2)
    st.write(f"Audio duration: {duration} seconds")

# Feature 6: Error Handling - API and Upload Errors
if uploaded_file is not None:
    st.info("Transcribing audio... Please wait.")
    try:
        result = transcribe_audio(uploaded_file)
    except Exception as e:
        log_error(str(e))
        st.error(f"Error occurred: {str(e)}")

    # Feature 7: Show detailed transcription result
    if "text" in result:
        st.success("Transcription Complete:")
        st.write(result["text"])

        # Feature 8: Display result in a scrollable container
        st.text_area("Transcription Result", result["text"], height=300)

        # Feature 9: Download transcription as text file
        transcription_text = result["text"]
        st.download_button(
            label="Download Transcription",
            data=transcription_text,
            file_name="transcription.txt",
            mime="text/plain"
        )

    # Feature 10: Show API response time
    response_time = time.time() - uploaded_file._timestamp
    st.write(f"API Response Time: {round(response_time, 2)} seconds")

    # Feature 11: Allow user to input specific language for transcription
    lang = st.selectbox("Select transcription language", ["en", "es", "fr", "de", "it", "pt", "zh"])
    if lang != "en":
        result = transcribe_audio(uploaded_file)  # Re-send the file with selected language (if API supports it)

    # Feature 12: Language auto-detection feedback
    if "error" in result:
        st.error(f"Error in transcribing audio. Please try again. Details: {result['error']}")

    # Feature 13: Display audio waveform visualization
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/mp3", start_time=0)

    # Feature 14: Play back the uploaded file after transcription
    st.audio(uploaded_file, format="audio/mp3")

# Feature 15: Enhance UI with a background image (e.g., waves, audio-related)
st.markdown("""
<style>
    .reportview-container {
        background-image: url("https://your-image-url.com/waves.jpg");
        background-size: cover;
        background-position: center;
    }
</style>
""", unsafe_allow_html=True)

# Feature 16: Add user profile (allow sign-in for saving results)
if st.button("Sign In"):
    username = st.text_input("Enter username:")
    password = st.text_input("Enter password:", type="password")
    st.success(f"Welcome back, {username}!")

# Feature 17: Save and retrieve transcriptions from user history
if st.button("View Past Transcriptions"):
    if os.path.exists("transcriptions_history.txt"):
        with open("transcriptions_history.txt", "r") as file:
            st.text_area("Past Transcriptions", file.read(), height=200)

# Feature 18: Add dark/light mode toggle
st.markdown(
    """
    <style>
    .dark-theme {
        background-color: black;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

# Feature 19: Add transcription speed setting
speed = st.slider("Select transcription speed", min_value=0.5, max_value=2.0, step=0.1)

# Feature 20: Add file renaming option
new_name = st.text_input("Rename file:", value=uploaded_file.name)
if new_name != uploaded_file.name:
    st.write(f"File renamed to: {new_name}")

# Feature 21: Error handling with retry mechanism
retry_button = st.button("Retry Transcription")
if retry_button:
    st.info("Retrying transcription...")
    result = transcribe_audio(uploaded_file)

# Feature 22: Add notification when transcription is complete
if "text" in result:
    st.success("Transcription complete! 🎉")

# Feature 23: Voice feedback on transcription completion
import pyttsx3
if "text" in result:
    engine = pyttsx3.init()
    engine.say("Transcription complete")
    engine.runAndWait()

# Feature 24: Provide a file download link (cloud storage link) for transcriptions
cloud_storage_link = "https://your-cloud-storage.com/your-transcription-link"
st.markdown(f"[Download from Cloud]({cloud_storage_link})")

# Feature 25: Provide additional metadata (e.g., speaker separation, timestamps, etc.)
if "text" in result:
    st.write(f"Transcription Metadata:")
    st.write(f"- Duration: {duration} seconds")
    st.write(f"- Language: {lang}")
    st.write(f"- Number of Words: {len(result['text'].split())}")

# End of the app
