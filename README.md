# OpenAI Image Generator Web App

This is a web application that uses OpenAI's DALL-E 3 API to generate images from text prompts. The app provides a user-friendly interface for creating AI-generated images with various customization options.

## Features

- Generate images from text prompts
- Customize image size (square, landscape, portrait)
- Select quality levels (standard, hd)
- Choose output format (PNG, JPEG, WebP)
- Option for natural style rendering
- Download generated images

## Prerequisites

- Python 3.8+
- OpenAI API key

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Run the application:
   ```
   python main.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a descriptive prompt for the image you want to generate
2. Configure the desired options:
   - Size: Select from square (1024×1024), landscape (1792×1024), or portrait (1024×1792)
   - Quality: Choose standard or HD (affects token usage and cost)
   - Format: Select PNG, JPEG, or WebP
   - Style: Select natural style (recommended for creative images)
3. Click "Generate Image" and wait for the result (can take up to 2 minutes)
4. Download your generated image using the "Download Image" button

## Important Notes

- Image generation costs vary based on the size and quality settings
- Higher quality settings will result in better images but take longer to generate
- You need a valid OpenAI API key with sufficient credits to use this application

## Technology Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- API: OpenAI DALL-E 3
- Styling: Bootstrap 5 