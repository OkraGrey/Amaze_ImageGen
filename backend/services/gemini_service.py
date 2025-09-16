"""
Service for interacting with Google's Gemini API.
"""
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
import uuid
from pathlib import Path

from backend.config.settings import GEMINI_API_KEY, GEMINI_MODEL, RESULT_DIR

class GeminiService:
    """Service for generating images using Google's Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
    
    def generate_image(self, prompt, image_path=None):
        """
        Generate an image based on the prompt and optionally an input image.
        
        Args:
            prompt (str): The text prompt for image generation
            image_path (str, optional): Path to an input image
            
        Returns:
            str: Path to the generated image
        """
        try:
            contents = [prompt]
            
            # Add image to contents if provided
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                contents.append(image)
            
            # Generate content
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            
            # Save the generated image
            result_path = None
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    # Generate a unique filename
                    filename = f"generated_{uuid.uuid4().hex}.png"
                    result_path = os.path.join(RESULT_DIR, filename)
                    
                    # Save the image
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(result_path)
                    break
            
            return result_path
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise
