import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
from PIL import Image
import time

# Configure Gemini API
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

# Streamlit UI
st.title("🎤 Vocal Eyes")

# Initialize session state for countdown
if 'countdown_started' not in st.session_state:
    st.session_state.countdown_started = False
    st.session_state.capture_time = None

# JavaScript for camera initialization and countdown
st.markdown(
    """
    <script>
        setTimeout(function() {
            var camInput = document.querySelector("input[type='file']");
            if (camInput) { camInput.click(); }
        }, 500);
    </script>
    """,
    unsafe_allow_html=True
)

# Camera input placeholder
camera_placeholder = st.empty()

# Start countdown if not already started
if not st.session_state.countdown_started:
    st.session_state.countdown_started = True
    st.session_state.capture_time = time.time() + 3

# Display countdown
if st.session_state.countdown_started and st.session_state.capture_time:
    remaining_time = max(0, int(st.session_state.capture_time - time.time()))
    if remaining_time > 0:
        st.write(f"📸 Capturing in {remaining_time} seconds...")
        time.sleep(1)
        st.experimental_rerun()
    else:
        # Capture image
        image_file = camera_placeholder.camera_input("Capturing...")
        
        if image_file:
            # Process the captured image
            image = Image.open(image_file)
            st.image(image, caption="Captured Image", use_column_width=True)
            
            # Generate and display image description
            description = generate_description(image)
            st.write(f"**📝 Description:** {description}")
            
            # Convert description to speech and play audio
            audio_path = text_to_speech(description)
            if audio_path:
                st.audio(audio_path, format="audio/mp3")
                
                # Auto close after speaking
                st.write("✅ **Closing in 5 seconds...**")
                time.sleep(5)
                # Reset session state and rerun
                st.session_state.countdown_started = False
                st.session_state.capture_time = None
                st.experimental_rerun()
