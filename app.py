import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
from PIL import Image
import time

# ✅ Configure Gemini API with error handling
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

def generate_description(image):
    """Generates an AI-based description for the given image."""
    try:
        response = model.generate_content(["Describe this image for a blind person in 20 words:", image])
        return response.text if response else "No description available"
    except Exception as e:
        return f"Error generating description: {str(e)}"

def text_to_speech(text):
    """Converts text to speech and returns the audio file path."""
    try:
        tts = gTTS(text=text, lang="en")
        tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(tts_path)
        return tts_path
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

# ✅ Streamlit UI
st.title("🎤 Vocal Eyes")

# ✅ Hidden Auto-Capture Mechanism
if "image_captured" not in st.session_state:
    st.session_state.image_captured = False

if not st.session_state.image_captured:
    st.write("📷 **Capturing image automatically in 3 seconds...**")
    time.sleep(3)
    image_file = st.camera_input("Auto Capture Enabled")
    if image_file:
        st.session_state.image_captured = True
else:
    image_file = st.camera_input("Capture or Upload an Image")

if image_file:
    # Open the image and display it
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Generate and display image description
    description = generate_description(image)
    st.write(f"**📝 Description:** {description}")

    # Convert description to speech and play audio
    audio_path = text_to_speech(description)
    if audio_path:
        st.audio(audio_path, format="audio/mp3")

        # ✅ Auto close after playing audio (5 sec delay)
        st.write("✅ **Closing in 5 seconds...**")
        time.sleep(5)
        st.session_state.image_captured = False  # Reset for next use
        st.experimental_rerun()  # Refresh the app to restart process
