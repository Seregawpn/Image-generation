import os
import requests
import json
import base64
import time
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

def generate_image(prompt, size="1024x1024", quality="standard", model="dall-e-3", n=1, format="png", background="auto"):
    """
    Generate an image using OpenAI's image generation API
    
    Args:
        prompt (str): The text prompt to generate an image from
        size (str): Image size (1024x1024, 1792x1024, 1024x1792)
        quality (str): Image quality (standard, hd)
        model (str): Model to use for generation
        n (int): Number of images to generate
        format (str): Output format (png, jpeg, webp)
        background (str): Background type (transparent or auto)
        
    Returns:
        dict: API response containing the generated image(s)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size,
        "quality": quality,
        "response_format": "b64_json"
    }
    
    if background == "transparent" and format in ["png", "webp"]:
        payload["style"] = "natural"
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling OpenAI API: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response: {e.response.text}")
        raise

def save_image(b64_image, filename):
    """Save a base64 encoded image to a file"""
    image_data = base64.b64decode(b64_image)
    with open(filename, "wb") as f:
        f.write(image_data)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def api_generate_image():
    data = request.json
    prompt = data.get('prompt', '')
    size = data.get('size', '1024x1024')
    quality = data.get('quality', 'standard')
    format = data.get('format', 'png')
    background = data.get('background', 'auto')
    
    try:
        response = generate_image(
            prompt=prompt,
            size=size,
            quality=quality,
            format=format,
            background=background
        )
        
        if not os.path.exists('static/images'):
            os.makedirs('static/images')
        
        image_paths = []
        for i, image_data in enumerate(response.get('data', [])):
            filename = f"static/images/generated_{i}_{int(time.time())}.{format}"
            save_image(image_data['b64_json'], filename)
            image_paths.append('/' + filename)
        
        return jsonify({
            'success': True,
            'images': image_paths
        })
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
