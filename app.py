import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
import base64
from PIL import Image
import io
import time
import streamlit.components.v1 as components

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
        response = model.generate_content(
            ["Describe this image in detail for a blind person in 40 words:", image]
        )
        return response.text if response else "No description available"
    except Exception as e:
        return f"Error generating description: {str(e)}"

def text_to_speech(text):
    """Converts text to speech using gTTS and returns the base64 audio string."""
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

st.title("🎤 Vocal Eyes")

# --- Custom HTML/JS Component for Rear-Camera Auto-Capture ---
# This component attempts to force the rear camera, waits 3 seconds, and captures an image.
# (Due to Streamlit’s current limitations, we cannot automatically retrieve the captured image.)
html_code = """
<html>
  <body>
    <video id="video" autoplay playsinline style="width:100%;"></video>
    <canvas id="canvas" style="display:none;"></canvas>
    <script>
      async function startCamera() {
          try {
              // Request rear camera only
              const stream = await navigator.mediaDevices.getUserMedia({ 
                  video: { facingMode: { exact: "environment" } } 
              });
              const video = document.getElementById("video");
              video.srcObject = stream;
          } catch(e) {
              console.error("Error accessing rear camera:", e);
          }
      }
      async function autoCapture() {
          await startCamera();
          // Wait 3 seconds for the camera to adjust
          setTimeout(() => {
              const video = document.getElementById("video");
              const canvas = document.getElementById("canvas");
              canvas.width = video.videoWidth;
              canvas.height = video.videoHeight;
              const ctx = canvas.getContext("2d");
              ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
              // Convert the captured image to a Base64 string
              const dataURL = canvas.toDataURL("image/png");
              // Post message with the captured image
              window.parent.postMessage(dataURL, "*");
          }, 3000);
      }
      autoCapture();
    </script>
  </body>
</html>
"""

# Render the HTML component.
# (Note: This does not automatically pass the image back to Streamlit.)
components.html(html_code, height=400)

st.info("If the auto-capture from the rear camera did not work, please use the fallback below.")

# --- Fallback: Use st.camera_input to let the user capture an image manually ---
# (User can manually select the rear camera if their device/browser allows.)
image_file = st.camera_input("Please capture an image using the rear camera")

if image_file:
    # Open and display the captured image
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)
    
    # Generate AI description
    description = generate_description(image)
    st.write(f"**📝 Description:** {description}")
    
    # Convert description to speech and auto-play it
    audio_base64 = text_to_speech(description)
    if audio_base64:
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
