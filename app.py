import streamlit as st
import google.generativeai as genai
from google.cloud import texttospeech
import os
import tempfile
import base64
from PIL import Image
import time

# ✅ Configure Gemini API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

# ✅ Configure Google Cloud TTS
if "GOOGLE_APPLICATION_CREDENTIALS" in st.secrets:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    client = texttospeech.TextToSpeechClient()
else:
    st.error("⚠️ Google Cloud TTS Key missing! Please set GOOGLE_APPLICATION_CREDENTIALS.")
    st.stop()

def generate_description(image):
    """Generates an AI-based description for the given image."""
    try:
        response = model.generate_content(["Describe this image in detail for a blind person in 40 words:", image])
        return response.text if response else "No description available"
    except Exception as e:
        return f"Error generating description: {str(e)}"

def google_tts(text):
    """Converts text to speech using Google Cloud TTS and returns audio file path."""
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        
        tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        with open(tts_path, "wb") as out:
            out.write(response.audio_content)
        
        return tts_path
    except Exception as e:
        st.error(f"Google TTS Error: {e}")
        return None

def autoplay_audio(file_path):
    """Encodes audio to Base64 and autoplays it."""
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

    # Inject JavaScript + HTML to autoplay
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# ✅ Streamlit UI
st.title("🎤 Vocal Eyes")

# ✅ JavaScript to auto-open camera (for mobile)
st.markdown(
    """
    <script>
        setTimeout(function() {
            var camInput = document.querySelector("input[type='file']");
            if (camInput) { camInput.click(); }
        }, 1000);
    </script>
    """,
    unsafe_allow_html=True
)

# ✅ Auto Capture Image
image_file = st.camera_input("Auto Capturing...")

if image_file:
    # Open the image and display it
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Generate and display image description
    description = generate_description(image)
    st.write(f"**📝 Description:** {description}")

    # Convert description to speech and autoplay
    audio_path = google_tts(description)
    if audio_path:
        autoplay_audio(audio_path)

        # ✅ Auto close after speaking
        st.write("✅ **Closing in 5 seconds...**")
        time.sleep(5)
        st.experimental_rerun()  # Refresh the app for the next capture
