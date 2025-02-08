import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
from PIL import Image
import time

# ✅ Configure Gemini API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

def generate_description(image):
    """Generates an AI-based description for the given image."""
    try:
        response = model.generate_content(["Describe this image in detail for a blind person in 40 words:", image])
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

    # Convert description to speech and play audio
    audio_path = text_to_speech(description)
    if audio_path:
        # ✅ JavaScript for Autoplay Audio
        st.markdown(
            f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{open(audio_path, "rb").read().encode("base64").decode()}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True
        )

        # ✅ Auto close after speaking
        st.write("✅ **Closing in 5 seconds...**")
        time.sleep(5)
        st.experimental_rerun()  # Refresh the app for the next capture
