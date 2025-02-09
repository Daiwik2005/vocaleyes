# # import streamlit as st
# # import google.generativeai as genai
# # from gtts import gTTS
# # import os
# # import tempfile
# # import base64
# # from PIL import Image
# # from streamlit_javascript import st_javascript

# # # ✅ Configure Gemini API
# # if "GEMINI_API_KEY" in st.secrets:
# #     genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# #     model = genai.GenerativeModel("gemini-1.5-flash")
# # else:
# #     st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
# #     st.stop()

# # def generate_description(image):
# #     """Generates an AI-based description for the given image."""
# #     try:
# #         response = model.generate_content(["Describe this image in detail for a blind person in 40 words:", image])
# #         return response.text if response else "No description available"
# #     except Exception as e:
# #         return f"Error generating description: {str(e)}"

# # def text_to_speech(text):
# #     """Converts text to speech using gTTS and returns the base64 audio string."""
# #     try:
# #         tts = gTTS(text=text, lang="en")
# #         tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
# #         tts.save(tts_path)
        
# #         # Convert to base64 for embedding in HTML
# #         with open(tts_path, "rb") as audio_file:
# #             audio_base64 = base64.b64encode(audio_file.read()).decode()

# #         # Remove temporary file
# #         os.remove(tts_path)
# #         return audio_base64
# #     except Exception as e:
# #         st.error(f"Text-to-speech error: {e}")
# #         return None

# # # ✅ Streamlit UI
# # st.title("🎤 Vocal Eyes")

# # # ✅ JavaScript for Long Press & Double Tap Camera Capture
# # gesture_script = """
# #     let pressTimer;
# #     let lastTap = 0;

# #     document.addEventListener("touchstart", function(event) {
# #         pressTimer = setTimeout(function() {
# #             window.dispatchEvent(new Event("longPress"));
# #         }, 1500); // Long press for 1.5 seconds
# #     });

# #     document.addEventListener("touchend", function(event) {
# #         clearTimeout(pressTimer);

# #         let currentTime = new Date().getTime();
# #         let tapLength = currentTime - lastTap;
# #         if (tapLength < 300 && tapLength > 0) {
# #             window.dispatchEvent(new Event("doubleTap"));
# #         }
# #         lastTap = currentTime;
# #     });

# #     window.addEventListener("longPress", function() {
# #         document.querySelector('input[type="file"]').click();
# #     });

# #     window.addEventListener("doubleTap", function() {
# #         let camInput = document.querySelector('input[type="file"]');
# #         if (camInput) {
# #             camInput.setAttribute('capture', 'environment'); // Switch to back camera
# #             camInput.click();
# #         }
# #     });
# # """

# # st_javascript(gesture_script)

# # # ✅ Camera input
# # image_file = st.camera_input("Long Press to Capture Image, Double Tap for Back Camera")

# # if image_file:
# #     # Open the image and display it
# #     image = Image.open(image_file)
# #     st.image(image, caption="Captured Image", use_column_width=True)

# #     # Generate and display image description
# #     description = generate_description(image)
# #     st.write(f"**📝 Description:** {description}")

# #     # Convert description to speech and play audio
# #     audio_base64 = text_to_speech(description)
    
# #     if audio_base64:
# #         # ✅ Embed base64 audio in HTML for auto-play
# #         audio_html = f"""
# #             <audio autoplay>
# #                 <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
# #             </audio>
# #         """
# #         st.markdown(audio_html, unsafe_allow_html=True)


# import streamlit as st
# import google.generativeai as genai
# from gtts import gTTS
# import os
# import tempfile
# import base64
# from PIL import Image
# from streamlit_javascript import st_javascript

# # ✅ Configure Gemini API
# if "GEMINI_API_KEY" in st.secrets:
#     genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
#     model = genai.GenerativeModel("gemini-1.5-flash")
# else:
#     st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
#     st.stop()

# def generate_description(image):
#     """Generates an AI-based description for the given image."""
#     try:
#         response = model.generate_content(["Describe this image in detail for a blind person in 40 words:", image])
#         return response.text if response else "No description available"
#     except Exception as e:
#         return f"Error generating description: {str(e)}"

# def text_to_speech(text):
#     """Converts text to speech using gTTS and returns the base64 audio string."""
#     try:
#         tts = gTTS(text=text, lang="en")
#         tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
#         tts.save(tts_path)
        
#         # Convert to base64 for embedding in HTML
#         with open(tts_path, "rb") as audio_file:
#             audio_base64 = base64.b64encode(audio_file.read()).decode()

#         # Remove temporary file
#         os.remove(tts_path)
#         return audio_base64
#     except Exception as e:
#         st.error(f"Text-to-speech error: {e}")
#         return None

# # ✅ Streamlit UI
# st.title("🎤 Vocal Eyes")

# # ✅ JavaScript for Long Press & Double Tap with polling to attach events
# # This script checks every 500ms for the file input element (from st.camera_input)
# # Once it finds it, it attaches touch event listeners.
# gesture_script = """
# (function() {
#     function attachListeners() {
#         let cameraInput = document.querySelector('input[type="file"]');
#         if (cameraInput) {
#             let pressTimer;
#             let lastTap = 0;
            
#             cameraInput.addEventListener("touchstart", function(event) {
#                 pressTimer = setTimeout(function() {
#                     // Long press detected: trigger click to open camera
#                     cameraInput.click();
#                 }, 1500); // 1.5 seconds for long press
#             });
            
#             cameraInput.addEventListener("touchend", function(event) {
#                 clearTimeout(pressTimer);
#                 let currentTime = new Date().getTime();
#                 let tapLength = currentTime - lastTap;
#                 if (tapLength < 300 && tapLength > 0) {
#                     // Double tap detected:
#                     // Attempt to switch to the back camera by setting the capture attribute to "environment"
#                     cameraInput.setAttribute('capture', 'environment');
#                     cameraInput.click();
#                 }
#                 lastTap = currentTime;
#             });
#             return true; // listeners attached
#         }
#         return false;
#     }
    
#     var intervalId = setInterval(function() {
#         if (attachListeners()) {
#             clearInterval(intervalId);
#         }
#     }, 500);
# })();
# """

# # Run the JS code
# st_javascript(gesture_script, key="gesture_js")

# # ✅ Camera input
# image_file = st.camera_input("Long Press to Capture Image, Double Tap for Back Camera")

# if image_file:
#     # Open the image and display it
#     image = Image.open(image_file)
#     st.image(image, caption="Captured Image", use_column_width=True)

#     # Generate and display image description
#     description = generate_description(image)
#     st.write(f"**📝 Description:** {description}")

#     # Convert description to speech and play audio
#     audio_base64 = text_to_speech(description)
    
#     if audio_base64:
#         # Embed base64 audio in HTML for auto-play
#         audio_html = f"""
#             <audio autoplay>
#                 <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#             </audio>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)


import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
import base64
from PIL import Image
from streamlit_javascript import st_javascript
from googletrans import Translator

# ✅ Configure Gemini API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

# ✅ Initialize Translator
translator = Translator()

# ✅ Define Supported Languages
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Tamil": "ta",
    "Bengali": "bn",
    "Marathi": "mr",
}

# ✅ Language Selection
selected_language = st.selectbox("🌍 Select Language:", list(LANGUAGES.keys()))

def generate_description(image):
    """Generates an AI-based description for the given image."""
    try:
        response = model.generate_content(["Describe this image in detail for a blind person in 40 words:", image])
        return response.text if response else "No description available"
    except Exception as e:
        return f"Error generating description: {str(e)}"

def translate_text(text, target_lang):
    """Translates text into the selected language."""
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"Translation error: {str(e)}"

def text_to_speech(text, lang_code):
    """Converts text to speech using gTTS and returns the base64 audio string."""
    try:
        tts = gTTS(text=text, lang=lang_code)
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
st.title("🎤 Vocal Eyes - Multilingual Support")

# ✅ Camera input
image_file = st.camera_input("📸 Capture Image")

if image_file:
    # Open the image and display it
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Generate and display image description
    description = generate_description(image)
    st.write(f"**📝 Description (English):** {description}")

    # Translate description
    translated_text = translate_text(description, LANGUAGES[selected_language])
    st.write(f"**🌍 Description ({selected_language}):** {translated_text}")

    # Convert translated text to speech
    audio_base64 = text_to_speech(translated_text, LANGUAGES[selected_language])

    if audio_base64:
        # Embed base64 audio in HTML for auto-play
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)


