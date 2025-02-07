# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import cv2
# import google.generativeai as genai
# import pyttsx3
# import os

# app = Flask(__name__)
# CORS(app)  # Allows frontend to call this backend API

# genai.configure(api_key=" AIzaSyDjEPSblr8blzV2UQGERglL7SlGWQINa3I")  # Replace with your API key
# model = genai.GenerativeModel("gemini-1.5-flash")

# def capture_image():
#     cam = cv2.VideoCapture(0)  # Open the webcam
#     ret, frame = cam.read()  # Capture a frame
#     if ret:
#         img_path = "captured_image.jpg"
#         cv2.imwrite(img_path, frame)
#         cam.release()
#         return img_path
#     cam.release()
#     return None

# def generate_description(image_path):
#     with open(image_path, "rb") as img:
#         response = model.generate_content(["Describe this image in a simple way:", img.read()])
#     return response.text if response else "No description available."

# def text_to_speech(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

# # @app.route("/capture", methods=["GET"])
# # def process_image():
# #     img_path = capture_image()
# #     if not img_path:
# #         return jsonify({"error": "Failed to capture image"}), 500
    
# #     description = generate_description(img_path)
# #     text_to_speech(description)

# #     os.remove(img_path)  # Clean up the image file after processing
# #     return jsonify({"message": "Spoken", "description": description})




# @app.route("/", methods=["GET"])
# def home():
#     return "Backend is running"

# @app.route("/capture", methods=["GET"])
# def process_image():
#     img_path = capture_image()
#     if not img_path:
#         return jsonify({"error": "Failed to capture image"}), 500
    
#     description = generate_description(img_path)
#     text_to_speech(description)

#     os.remove(img_path)  # Clean up the image file after processing
#     return jsonify({"message": "Spoken", "description": description})

# if __name__ == "__main__":
#     app.run(debug=True)









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
