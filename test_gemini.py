"""
Test script for the Gemini service.
"""
import os
from dotenv import load_dotenv
from backend.services.gemini_service import GeminiService

def test_gemini_service():
    """Test the Gemini service with a simple prompt."""
    # Initialize the service
    service = GeminiService()
    
    # Test with prompt only
    prompt = "Create a picture of a cat wearing a hat"
    print(f"Testing with prompt: {prompt}")
    
    try:
        result_path = service.generate_image(prompt)
        if result_path and os.path.exists(result_path):
            print(f"✅ Image generated successfully: {result_path}")
        else:
            print("❌ Failed to generate image")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test with prompt and image
    sample_image = "Rock/rock_1.png"
    if os.path.exists(sample_image):
        prompt = "Use this image but make the background blue"
        print(f"\nTesting with prompt and image: {prompt}")
        
        try:
            result_path = service.generate_image(prompt, sample_image)
            if result_path and os.path.exists(result_path):
                print(f"✅ Image generated successfully: {result_path}")
            else:
                print("❌ Failed to generate image")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print(f"\n❌ Sample image not found: {sample_image}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if API key is available
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please create a .env file with your API key")
        exit(1)
    
    # Run the test
    test_gemini_service()
