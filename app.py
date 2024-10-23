from flask import Flask, render_template, request
import requests

app = Flask(__name__)

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
    # Get selected values with defaults
    selected_size = request.form.get('size', '1024x1024')  # Default value
    selected_style = request.form.get('style', 'vivid')    # Default value
    selected_quality = request.form.get('quality', 'standard')  # Default value
    
    if request.method == 'POST':
        prompt = request.form.get('prompt')

        if prompt:
            result = generate_image(prompt, selected_size, selected_style, selected_quality)

            if 'error' in result:
                return render_template('index.html', error=result['error'],
                                       selected_size=selected_size, selected_style=selected_style, selected_quality=selected_quality)
            else:
                image_url = result.get('data')[0].get('url')  
                return render_template('index.html', image_url=image_url,
                                       selected_size=selected_size, selected_style=selected_style, selected_quality=selected_quality)
        else:
            return render_template('index.html', error="Please provide a prompt.",
                                   selected_size=selected_size, selected_style=selected_style, selected_quality=selected_quality)

    return render_template('index.html', selected_size=selected_size, selected_style=selected_style, selected_quality=selected_quality)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
