from flask import Flask, render_template, request, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Azure OpenAI API details
endpoint = "https://ai-jcu-demo.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
api_key = "abd5d70f5a2a4df18aef7e8ccfeacf02"

# Function to generate image from Azure AI
def generate_image(prompt, size, style, quality):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    data = {
        "prompt": prompt,
        "size": size,
        "style": style,
        "quality": quality
    }
    response = requests.post(endpoint, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

# Route to display HTML form for entering the prompt
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the prompt, size, style, and quality from the form submission
        prompt = request.form.get('prompt')
        size = request.form.get('size')
        style = request.form.get('style')
        quality = request.form.get('quality')
        
        if prompt:
            # Generate the image using the Azure API with size, style, and quality
            result = generate_image(prompt, size, style, quality)
            
            # Handle the result, including any errors
            if 'error' in result:
                return render_template('index.html', error=result['error'], previous_images=session.get('previous_images', []))
            else:
                # Extract the image URL or relevant data from the response
                image_url = result.get('data')[0].get('url')  # Example of handling response

                # Store image URL in session to keep track of previous images
                if 'previous_images' not in session:
                    session['previous_images'] = []
                
                session['previous_images'].insert(0, image_url)  # Add new image at the beginning of the list

                return render_template('index.html', image_url=image_url, previous_images=session['previous_images'])
        else:
            return render_template('index.html', error="Please provide a prompt.", previous_images=session.get('previous_images', []))
    
    return render_template('index.html', previous_images=session.get('previous_images', []))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
