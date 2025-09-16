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
from backend.services.base_service import BaseImageGenerationService

class GeminiService(BaseImageGenerationService):    
    def __init__(self):
        print(f"[INFO]---INITIALIZING GEMINI SERVICE---")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
    
    def generate_image(self, prompt, image_path=None):

        try:
            contents = [prompt]
            if image_path and os.path.exists(image_path):
                print(f"[INFO]---RECIEVED IMAGE PATH---")
                image = Image.open(image_path)
                contents.append(image)
            else:
                print(f"[INFO]---NO IMAGE PATH PROVIDED. GOING FORWARD WITH PROMPT ONLY---")
            
            print(f"[INFO]---CALLING GEMINI CLIENT---")
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            
            # Save the generated image
            print(f"[INFO]---SAVING THE GENERATED IMAGE---")
            result_path = None
            # print(f"[INFO]---RESPONSE RECIEVED FROM GEMINI CLIENT: {response}---")
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    # Generate a unique filename
                    filename = f"generated_{uuid.uuid4().hex}.png"
                    result_path = os.path.join(RESULT_DIR, filename)
                    
                    # Save the image
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(result_path)
                    print(f"[INFO]---IMAGE SAVED SUCCESSFULLY AT: {result_path}---")
                    break
            return result_path
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise
