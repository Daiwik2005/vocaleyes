import streamlit as st
import cv2
import numpy as np
import time
import tempfile
import os
import base64
from PIL import Image
import google.generativeai as genai
from gtts import gTTS
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# --- Configure Gemini API ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

def generate_description(image):
    """Generates an AI-based description for the given image."""
    try:
        response = model.generate_content([
            "Describe this image in detail for a blind person in 40 words:",
            image
        ])
        return response.text if response else "No description available"
    except Exception as e:
        return f"Error generating description: {str(e)}"

def text_to_speech(text):
    """Converts text to speech using gTTS and returns a base64-encoded MP3 string."""
    try:
        tts = gTTS(text=text, lang="en")
        tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(tts_path)
        with open(tts_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode()
        os.remove(tts_path)
        return audio_base64
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

# --- Define a VideoTransformer to auto-capture a frame ---
class AutoCaptureTransformer(VideoTransformerBase):
    def __init__(self):
        self.captured_frame = None
        self.start_time = time.time()
        self.capture_done = False

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # After 3 seconds, capture one frame and mark done
        if not self.capture_done and (time.time() - self.start_time) > 3:
            self.captured_frame = img.copy()
            self.capture_done = True
        return img

st.title("🎤 Vocal Eyes")

# --- Start the webrtc streamer with rear camera constraint ---
ctx = webrtc_streamer(
    key="vocal-eyes",
    video_transformer_factory=AutoCaptureTransformer,
    media_stream_constraints={"video": {"facingMode": "environment"}},
    desired_playing_state=True,
)

# --- Once a frame is captured, process it ---
if ctx.video_transformer:
    transformer = ctx.video_transformer
    if transformer.capture_done and transformer.captured_frame is not None:
        # Convert the captured frame (BGR) to a PIL image (RGB)
        frame = transformer.captured_frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        st.image(image, caption="Captured Image", use_column_width=True)
        
        # Generate AI description
        description = generate_description(image)
        st.write(f"**📝 Description:** {description}")
        
        # Convert description to speech and autoplay audio
        audio_base64 = text_to_speech(description)
        if audio_base64:
            audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
        
        st.info("Auto-capture complete. Refresh the page to try again.")
