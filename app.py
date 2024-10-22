from flask import Flask, render_template, request
import requests
import json
from io import BytesIO
from PIL import Image
import base64
import os

# Load API key from environment variable for security
API_URL = "https://ai-jcu-demo.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
API_KEY = os.getenv("AZURE_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("prompt")
        
        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }
        
        data = {
            "prompt": user_input,
            "n": 1,
            "size": "1024x1024"
        }
        
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200 and "data" in response_data:
            image_data = response_data["data"][0]["b64_json"]
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            
            img_io = BytesIO()
            image.save(img_io, 'PNG')
            img_io.seek(0)
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

            return render_template("index.html", img_data=img_base64)
        else:
            return "Error generating image.", 500
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)  # Ensure debug is set to False in production
