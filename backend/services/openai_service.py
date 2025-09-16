from openai import OpenAI
import base64
from dotenv import load_dotenv
import os
load_dotenv()
from backend.services.base_service import BaseImageGenerationService
from PIL import Image
from io import BytesIO
import os
import uuid
from pathlib import Path
from backend.config.settings import RESULT_DIR
class OpenAIService(BaseImageGenerationService):    
    def __init__(self):
        print(f"[INFO]---INITIALIZING OPENAI SERVICE---")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = 'gpt-image-1'
    
    def generate_image(self, prompt, image_path=None):

        print(f"[INFO]---RECIEVED PROMPT: {prompt}---")
        try:
            result = None
            if image_path and os.path.exists(image_path):
                print(f"[INFO]---RECIEVED IMAGE PATH---")
                result = self.client.images.edit(
                    model="gpt-image-1",
                    image=[open(image_path, "rb")],
                    prompt=prompt,
                    input_fidelity="high",
                    quality="high"
                )
            else:
                print(f"[INFO]---NO IMAGE PATH PROVIDED. GOING FORWARD WITH PROMPT ONLY---")
                
                result = self.client.images.generate(
                    model="gpt-image-1",
                    prompt=prompt,
                    quality="high"
                )
            
            print(f"[INFO]---SAVING THE GENERATED IMAGE---")
            result_path = None
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            # Generate a unique filename
            filename = f"generated_{uuid.uuid4().hex}.png"
            result_path = os.path.join(RESULT_DIR, filename)
            with open(result_path, "wb") as f:
                f.write(image_bytes)
            print(f"[INFO]---IMAGE SAVED SUCCESSFULLY AT: {result_path}---")
            return result_path
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise



# result = client.images.edit(
#     model="gpt-image-1",
#     image=[open("results\generated_eb1b2154405945cea3d102550b6f1593.png", "rb")],
#     prompt="Preserve the logo and whatever is printed on the front side of the shirt. Remove everything else.",
#     input_fidelity="high",
#     background="transparent"
# )

# image_base64 = result.data[0].b64_json
# image_bytes = base64.b64decode(image_base64)

# # Save the image to a file
# with open("sprite.png", "wb") as f:
#     f.write(image_bytes)