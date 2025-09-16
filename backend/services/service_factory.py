from .base_service import BaseImageGenerationService
from .gemini_service import GeminiService
from .openai_service import OpenAIService

# A registry of available services
SERVICES = {
    "gemini": GeminiService(),
    "openai": OpenAIService(),
}

def get_service(model_name: str) -> BaseImageGenerationService:
    """
    Returns an instance of an image generation service based on the model name.
    """
    print(f"---RECEIVED MODEL NAME IN GET SERVICE: {model_name}---")
    print(f"---ALLOWED MODELs : {SERVICES.keys()}---")
    service = SERVICES.get(model_name.lower())
    if not service:
        raise ValueError(f"Unsupported model: {model_name}")
    return service
