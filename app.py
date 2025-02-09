import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
import base64
from PIL import Image

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
    """Converts text to speech using gTTS and returns the base64 audio string."""
    try:
        tts = gTTS(text=text, lang="en")
        tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(tts_path)
        
        # Convert to base64 for embedding in HTML
        with open(tts_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode()

        # Remove temporary file
        os.remove(tts_path)
        return audio_base64
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

# ✅ Streamlit UI
st.title("🎤 Vocal Eyes")

# ✅ JavaScript for Long Press & Double Tap Camera Capture
st.markdown("""
    <script>
        let pressTimer;
        let lastTap = 0;
        
        document.addEventListener("touchstart", function(event) {
            pressTimer = setTimeout(function() {
                var camButton = document.querySelector('.stCamera button');
                if (camButton) {
                    camButton.click();
                    setTimeout(function() {
                        var captureButton = document.querySelector('.stCamera button[data-testid="camera-button"]');
                        if (captureButton) {
                            captureButton.click();
                        }
                    }, 500); // Delay to allow camera to open
                }
            }, 1500); // Long press for 1.5 seconds
        });

        document.addEventListener("touchend", function(event) {
            clearTimeout(pressTimer);
            
            let currentTime = new Date().getTime();
            let tapLength = currentTime - lastTap;
            if (tapLength < 300 && tapLength > 0) {
                // Double Tap Detected
                var cameraInput = document.querySelector('input[type="file"]');
                if (cameraInput) {
                    cameraInput.setAttribute('capture', 'environment'); // Switch to back camera
                    cameraInput.click();
                }
            }
            lastTap = currentTime;
        });
    </script>
""", unsafe_allow_html=True)

# ✅ Camera input
image_file = st.camera_input("Long Press to Capture Image, Double Tap for Back Camera")

if image_file:
    # Open the image and display it
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Generate and display image description
    description = generate_description(image)
    st.write(f"**📝 Description:** {description}")

    # Convert description to speech and play audio
    audio_base64 = text_to_speech(description)
    
    if audio_base64:
        # ✅ Embed base64 audio in HTML for auto-play
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
