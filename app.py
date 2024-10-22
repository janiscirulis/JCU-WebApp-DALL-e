from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Azure OpenAI API details
endpoint = "https://ai-jcu-demo.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
api_key = "abd5d70f5a2a4df18aef7e8ccfeacf02"

# Function to generate image from Azure AI
def generate_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    data = {
        "prompt": prompt,
        "size": "1024x1024"  # You can adjust the image size as needed
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
        # Get the prompt from the form submission
        prompt = request.form.get('prompt')
        additional_comments = request.form.get('additional_comments', '')
        
        if prompt:
            # Create a full prompt including additional comments
            full_prompt = f"{prompt} {additional_comments}".strip()
            # Generate the image using the Azure API
            result = generate_image(full_prompt)
            
            # Handle the result, including any errors
            if 'error' in result:
                return render_template('index.html', error=result['error'], prompt=prompt)
            else:
                # Extract the image URL or relevant data from the response
                image_url = result.get('data')[0].get('url')  # Example of handling response
                
                return render_template('index.html', image_url=image_url, prompt=prompt, additional_comments=additional_comments)
        else:
            return render_template('index.html', error="Please provide a prompt.")
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
