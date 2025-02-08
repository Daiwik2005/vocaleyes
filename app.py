from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import google.generativeai as genai
import pyttsx3
import os
import threading

app = Flask(__name__)
CORS(app)

# Configure Gemini API (replace with your actual key)
genai.configure(api_key="AIzaSyDjEPSblr8blzV2UQGERglL7SlGWQINa3I")
model = genai.GenerativeModel("gemini-1.5-flash")

def capture_image():
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return None
        ret, frame = cam.read()
        cam.release()
        if ret:
            img_path = "captured_image.jpg"
            cv2.imwrite(img_path, frame)
            return img_path
    except Exception as e:
        print(f"Image capture error: {e}")
    return None

import io
from PIL import Image

def generate_description(image_path):
    try:
        # Open image using Pillow
        with Image.open(image_path) as img:
            # Generate description using Gemini API
            response = model.generate_content([
                "Describe this image in a simple, clear way:", 
                img
            ])
            
            return response.text if response else "No description available"
    
    except Exception as e:
        print(f"Image description error: {e}")
        return f"Error generating description: {str(e)}"

def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")

@app.route("/", methods=["GET"])
def process_image():
    img_path = capture_image()
    if not img_path:
        return jsonify({"error": "Failed to capture image"}), 500
    
    description = generate_description(img_path)
    
    # Use threading to avoid blocking
    threading.Thread(target=text_to_speech, args=(description,)).start()

    os.remove(img_path)  # Clean up the image file
    return jsonify({"message": "Image processed", "description": description})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
