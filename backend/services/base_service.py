from abc import ABC, abstractmethod

class BaseImageGenerationService(ABC):
    """Abstract base class for image generation services."""

    @abstractmethod
    def generate_image(self, prompt: str, image_path: str = None) -> str:
        """
        Generate an image based on a prompt and an optional input image.
        
        Args:
            prompt (str): The text prompt for generation.
            image_path (str, optional): The path to an input image.
            
        Returns:
            str: The path to the generated image.
        """
        pass
