
# # import streamlit as st
# # import google.generativeai as genai
# # from gtts import gTTS
# # import os
# # import tempfile
# # import base64
# # from PIL import Image
# # from deep_translator import GoogleTranslator  # ✅ Translation support

# # # ✅ Configure Gemini API
# # if "GEMINI_API_KEY" in st.secrets:
# #     genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# #     model = genai.GenerativeModel("gemini-1.5-flash")
# # else:
# #     st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
# #     st.stop()

# # # ✅ Language selection dropdown
# # language_options = {
# #     "English": "en",
# #     "Hindi (हिंदी)": "hi",
# #     "Marathi (मराठी)": "mr",
# #     "Tamil (தமிழ்)": "ta",
# #     "Telugu (తెలుగు)": "te",
# #     "Bengali (বাংলা)": "bn",
# #     "Gujarati (ગુજરાતી)": "gu",
# #     "Kannada (ಕನ್ನಡ)": "kn",
# #     "Punjabi (ਪੰਜਾਬੀ)": "pa",
# #     "Malayalam (മലയാളം)": "ml"
# # }

# # selected_language = st.selectbox("Choose a language for speech output:", list(language_options.keys()))
# # selected_lang_code = language_options[selected_language]

# # def generate_description(image):
# #     """Generates an AI-based description for the given image."""
# #     try:
# #         response = model.generate_content(["Describe this image in detail for a blind person in 40 words:", image])
# #         return response.text if response else "No description available"
# #     except Exception as e:
# #         return f"Error generating description: {str(e)}"

# # def translate_text(text, target_lang):
# #     """Translates text to the target language."""
# #     try:
# #         translated_text = GoogleTranslator(source="auto", target=target_lang).translate(text)
# #         return translated_text
# #     except Exception as e:
# #         st.error(f"Translation error: {e}")
# #         return text  # Return original text if translation fails

# # def text_to_speech(text, lang_code):
# #     """Converts text to speech using gTTS and returns the base64 audio string."""
# #     try:
# #         tts = gTTS(text=text, lang=lang_code)
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

# # # ✅ Camera input
# # image_file = st.camera_input("Capture Image")

# # if image_file:
# #     # Open the image and display it
# #     image = Image.open(image_file)
# #     st.image(image, caption="Captured Image", use_column_width=True)

# #     # Generate and display image description
# #     description = generate_description(image)
# #     st.write(f"**📝 English Description:** {description}")

# #     # ✅ Translate description before TTS
# #     translated_description = translate_text(description, selected_lang_code)
# #     st.write(f"**🌍 Translated Description:** {translated_description}")

# #     # Convert translated description to speech
# #     audio_base64 = text_to_speech(translated_description, selected_lang_code)
    
# #     if audio_base64:
# #         # Embed base64 audio in HTML for auto-play
# #         audio_html = f"""
# #             <audio autoplay>
# #                 <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
# #             </audio>
# #         """
# #         st.markdown(audio_html, unsafe_allow_html=True)


# # import streamlit as st
# # import google.generativeai as genai
# # from gtts import gTTS
# # import os
# # import tempfile
# # import base64
# # from PIL import Image
# # from streamlit_javascript import st_javascript
# # from deep_translator import GoogleTranslator

# # # ✅ Configure Gemini API
# # if "GEMINI_API_KEY" in st.secrets:
# #     genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# #     model = genai.GenerativeModel("gemini-1.5-flash")
# # else:
# #     st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
# #     st.stop()

# # # ✅ Supported Languages Mapping
# # language_options = {
# #     "en": "English",
# #     "hi": "Hindi (हिंदी)",
# #     "mr": "Marathi (मराठी)",
# #     "ta": "Tamil (தமிழ்)",
# #     "te": "Telugu (తెలుగు)",
# #     "bn": "Bengali (বাংলা)",
# #     "gu": "Gujarati (ગુજરાતી)",
# #     "kn": "Kannada (ಕನ್ನಡ)",
# #     "pa": "Punjabi (ਪੰਜਾਬੀ)",
# #     "ml": "Malayalam (മലയാളം)"
# # }

# # # ✅ Detect Browser Language (JavaScript)
# # user_lang = st_javascript("navigator.language || navigator.userLanguage;")[:2]  # Extract first 2 letters

# # # ✅ Set Detected Language (Default to English if unsupported)
# # selected_lang_code = user_lang if user_lang in language_options else "en"
# # selected_language = language_options[selected_lang_code]

# # st.write(f"🌍 Auto-detected Language: **{selected_language}**")

# # def generate_description(image):
# #     """Generates an AI-based description for the given image."""
# #     try:
# #         response = model.generate_content(["Describe this image in detail for a blind person in 40 words:", image])
# #         return response.text if response else "No description available"
# #     except Exception as e:
# #         return f"Error generating description: {str(e)}"

# # def translate_text(text, target_lang):
# #     """Translate text if the selected language is not English."""
# #     if target_lang != "en":
# #         try:
# #             return GoogleTranslator(source="en", target=target_lang).translate(text)
# #         except Exception as e:
# #             st.error(f"Translation error: {e}")
# #             return text  # Return original text if translation fails
# #     return text

# # def text_to_speech(text, lang_code):
# #     """Converts text to speech using gTTS and returns the base64 audio string."""
# #     try:
# #         tts = gTTS(text=text, lang=lang_code)
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

# # # ✅ Camera input
# # image_file = st.camera_input("Capture Image")

# # if image_file:
# #     # Open the image and display it
# #     image = Image.open(image_file)
# #     st.image(image, caption="Captured Image", use_column_width=True)

# #     # Generate and display image description
# #     description = generate_description(image)
# #     st.write(f"**📝 Description (English):** {description}")

# #     # Translate if needed
# #     translated_description = translate_text(description, selected_lang_code)
# #     st.write(f"**🌎 Translated Description ({selected_language}):** {translated_description}")

# #     # Convert description to speech in selected language
# #     audio_base64 = text_to_speech(translated_description, selected_lang_code)
    
# #     if audio_base64:
# #         # Embed base64 audio in HTML for auto-play
# #         audio_html = f"""
# #             <audio autoplay>
# #                 <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
# #             </audio>
# #         """
# #         st.markdown(audio_html, unsafe_allow_html=True)



import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
import base64
from PIL import Image
from streamlit_javascript import st_javascript
from deep_translator import GoogleTranslator

# ✅ Configure Gemini API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Key not found! Please check Streamlit Secrets.")
    st.stop()

# ✅ Supported Languages Mapping
language_options = {
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "mr": "Marathi (मराठी)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "bn": "Bengali (বাংলা)",
    "gu": "Gujarati (ગુજરાતી)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "ml": "Malayalam (മലയാളം)"
}

# ✅ Detect Browser Language (JavaScript)
user_lang = st_javascript("navigator.language || navigator.userLanguage;")[:2]  # Extract first 2 letters

# ✅ Set Detected Language (Default to English if unsupported)
selected_lang_code = user_lang if user_lang in language_options else "en"
selected_language = language_options[selected_lang_code]

st.write(f"🌍 Auto-detected Language: **{selected_language}**")

def generate_description(image):
    """Generates an AI-based description for the given image."""
    try:
        response = model.generate_content(["Describe this image in detail for a blind person in 40 words: and also if possible give me the distance of the object you can display max (in feets). if you cant measure the distance or if the pic is not clear tell me to take the pic directly again", image])
        return response.text if response else "No description available"
    except Exception as e:
        return f"Error generating description: {str(e)}"

def translate_text(text, target_lang):
    """Translate text if the selected language is not English."""
    if target_lang != "en":
        try:
            return GoogleTranslator(source="en", target=target_lang).translate(text)
        except Exception as e:
            st.error(f"Translation error: {e}")
            return text  # Return original text if translation fails
    return text

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
st.title("🎤 Vocal Eyes")
# ✅ Camera input
image_file = st.camera_input("Capture Image")

if image_file:
    # Open the image and display it
    image = Image.open(image_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Generate and display image description
    description = generate_description(image)
    st.write(f"**📝 Description (English):** {description}")

    # Translate if needed
    translated_description = translate_text(description, selected_lang_code)
    st.write(f"**🌎 Translated Description ({selected_language}):** {translated_description}")

    # Convert description to speech in selected language
    audio_base64 = text_to_speech(translated_description, selected_lang_code)
    
    if audio_base64:
        # Embed base64 audio in HTML for auto-play
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

