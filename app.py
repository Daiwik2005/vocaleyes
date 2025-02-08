

# import streamlit as st
# import google.generativeai as genai
# from gtts import gTTS
# import os
# import tempfile
# from PIL import Image

# # ✅ Configure Gemini API with error handling
# if "GEMINI_API_KEY" in st.secrets:
#     genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
#     model = genai.GenerativeModel("gemini-1.5-flash")
# else:
#     st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
#     st.stop()

# def generate_description(image):
#     """Generates an AI-based description for the given image."""
#     try:
#         response = model.generate_content(["Describe this image for a blind person in 20-25 words:", image])
#         return response.text if response else "No description available"
#     except Exception as e:
#         return f"Error generating description: {str(e)}"

# def text_to_speech(text):
#     """Converts text to speech and returns the audio file path."""
#     try:
#         tts = gTTS(text=text, lang="en")
#         tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
#         tts.save(tts_path)
#         return tts_path
#     except Exception as e:
#         st.error(f"Text-to-speech error: {e}")
#         return None

# # ✅ Streamlit UI
# st.title("🎤 Vocal Eyes")

# # ✅ Use Streamlit Camera Input (better for web apps)
# image_file = st.camera_input("📷 Capture or Upload an Image")

# if image_file:
#     # Open the image and display it
#     image = Image.open(image_file)
#     st.image(image, caption="Captured Image", use_column_width=True)

#     # Generate and display image description
#     description = generate_description(image)
#     st.write(f"**📝 Description:** {description}")

#     # Convert description to speech and play audio
#     audio_path = text_to_speech(description)
#     if audio_path:
#         st.audio(audio_path, format="audio/mp3")

#     # Cleanup (optional)
#     os.remove(audio_path)



import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
from PIL import Image
import base64
import time

# ✅ Configure Gemini API with error handling
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

# ✅ Inject JavaScript to auto-capture image using back camera
st.markdown("""
    <script>
    function captureImage() {
        let video = document.createElement("video");
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(stream => {
            video.srcObject = stream;
            video.play();
            setTimeout(() => {
                let canvas = document.createElement("canvas");
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext("2d").drawImage(video, 0, 0);
                let image_data = canvas.toDataURL("image/png");
                stream.getTracks().forEach(track => track.stop()); // Stop camera
                window.parent.postMessage(image_data, "*");
            }, 2000); // Auto-capture in 2 seconds
        });
    }
    window.onload = captureImage;
    </script>
""", unsafe_allow_html=True)

# ✅ Listen for auto-captured image from JavaScript
image_data = st.text_input("Hidden Image Data", key="image_data", type="default")

if image_data:
    # Convert Base64 to Image
    image_bytes = base64.b64decode(image_data.split(",")[1])
    img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    with open(img_path, "wb") as f:
        f.write(image_bytes)

    # Display the image
    image = Image.open(img_path)
    st.image(image, caption="Captured Image", use_column_width=True)

    # ✅ Generate and display image description
    description = "Generated description..."  # Placeholder for AI-generated text
    st.write(f"**📝 Description:** {description}")

    # ✅ Convert description to speech & auto-play
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    gTTS(text=description, lang="en").save(audio_path)

    # Auto-play the audio
    audio_base64 = base64.b64encode(open(audio_path, "rb").read()).decode()
    st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

    # ✅ Auto-close after playing audio
    time.sleep(5)  # Wait for audio to play
    st.markdown('<script>window.close();</script>', unsafe_allow_html=True)

    # Cleanup
    os.remove(audio_path)
    os.remove(img_path)




