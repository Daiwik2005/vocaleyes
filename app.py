

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
import base64
import os
import tempfile
from PIL import Image
from io import BytesIO

# ✅ Configure Gemini API
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ JavaScript to capture image and send it to Streamlit
st.markdown(
    """
    <script>
    function captureImage() {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(stream => {
            let video = document.createElement("video");
            video.srcObject = stream;
            video.play();
            setTimeout(() => {
                let canvas = document.createElement("canvas");
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                let ctx = canvas.getContext("2d");
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                let image_data = canvas.toDataURL("image/png");
                stream.getTracks().forEach(track => track.stop()); // Stop camera
                document.getElementById("image_data").value = image_data;
                document.getElementById("submit_button").click(); // Auto-submit
            }, 3000); // Capture after 3 seconds
        });
    }
    window.onload = captureImage;
    </script>
    """,
    unsafe_allow_html=True,
)

# ✅ Hidden input field to store captured image
image_data = st.text_input("Hidden Image Data", key="image_data")
st.markdown('<button id="submit_button" style="display:none;">Submit</button>', unsafe_allow_html=True)

if image_data and "," in image_data:
    try:
        # ✅ Decode Base64 image
        image_bytes = base64.b64decode(image_data.split(",")[1])
        img = Image.open(BytesIO(image_bytes))

        # ✅ Display the captured image
        st.image(img, caption="📷 Captured Image", use_column_width=True)

        # ✅ Generate AI description
        response = model.generate_content(["Describe this image for a blind person in 20-25 words:", img])
        description = response.text if response else "No description available."
        st.write(f"**📝 Description:** {description}")

        # ✅ Convert description to speech
        tts = gTTS(text=description, lang="en")
        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(audio_path)
        audio_base64 = base64.b64encode(open(audio_path, "rb").read()).decode()

        st.markdown(
            f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True,
        )

        # ✅ Close app after 5 seconds
        st.markdown('<script>setTimeout(() => window.close(), 5000);</script>', unsafe_allow_html=True)

        # Cleanup
        os.remove(audio_path)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
