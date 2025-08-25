Hello!

This is VocalEyes

Vocal Eyes is a minimalist accessibility web app designed to help blind and visually impaired users understand their surroundings.
It allows users to trigger the app with a voice command (“Scan”), capture a photo automatically, generate a description of the scene using AI, and then listen to the description via text-to-speech — all in a seamless flow.

Features

🧠 AI-Powered Description – Generates a short description of the scene.<br>
🔊 Text-to-Speech – Reads the description out loud.<br>
🔒 Minimal UI – Designed for accessibility and ease of use.<br>
🌍 Multi-Language Support – Works in 10+ languages, configurable by the user.<br>
🤖 Google Assistant Integration – Open the app by saying “Scan”.<br>


🚀 Getting Started

1. Clone the repository

```Bash
git clone https://github.com/Daiwik2005/vocal-eyes.git
cd vocal-eyes
```

2. Install dependencies

```Bash
pip install -r requirements.txt
```

3. Add your API keys (Important)

Streamlit requires secrets to be stored in a .streamlit/secrets.toml file.
Create a folder named .streamlit in your project root and add a secrets.toml file like this:

<h4># .streamlit/secrets.toml</h4>
```Bash
[api_keys]
gemini_api = "your_gemini_api_key_here"
# Add other keys here if needed
```


🔑 Without this file, the app will not work.

4. Run the app

```Bash
streamlit run app.py
```



🛠️ Tech Stack

Frontend: Streamlit (minimalist web UI)<br>
AI Model: Google Gemini API (for image description)<br>
TTS: Streamlit / Python text-to-speech libraries<br>
Voice Assistant: Google Assistant Action to launch app<br>

Enjoy!!