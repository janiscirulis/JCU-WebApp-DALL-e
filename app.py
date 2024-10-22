from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Azure OpenAI API details
endpoint = "https://ai-jcu-demo.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
api_key = "abd5d70f5a2a4df18aef7e8ccfeacf02"

# List to store generated images and prompts
generated_images = []

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
        # Check if it's an image update or a new image generation
        if 'update_image' in request.form:
            index = int(request.form.get('image_index'))
            new_prompt = request.form.get('new_prompt')
            additional_comments = request.form.get('additional_comments', '')
            
            # Update the existing prompt
            if generated_images:
                full_prompt = f"{new_prompt} {additional_comments}".strip()
                result = generate_image(full_prompt)
                
                if 'error' in result:
                    return render_template('index.html', error=result['error'], generated_images=generated_images)
                
                # Update the image URL in the list
                generated_images[index]['url'] = result.get('data')[0].get('url')
                generated_images[index]['prompt'] = full_prompt
            
        else:
            # Handle new image generation
            prompt = request.form.get('prompt')
            additional_comments = request.form.get('additional_comments', '')
            
            if prompt:
                full_prompt = f"{prompt} {additional_comments}".strip()
                result = generate_image(full_prompt)
                
                if 'error' in result:
                    return render_template('index.html', error=result['error'], generated_images=generated_images)
                
                # Add the new image to the list
                image_url = result.get('data')[0].get('url')
                generated_images.append({'prompt': full_prompt, 'url': image_url})
        
        return render_template('index.html', generated_images=generated_images)

    return render_template('index.html', generated_images=generated_images)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
