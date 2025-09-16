# Backend Documentation

This document provides an overview of the backend architecture, services, and API endpoints.

## Folder Structure

The backend is organized into the following main directories:

-   `config/`: Contains configuration files, such as `settings.py` for managing API keys and application-level settings.
-   `routes/`: Defines the API endpoints. Each file in this directory should group related endpoints.
-   `services/`: Holds the business logic. This is where interactions with external APIs (like Google Gemini) and core functionalities are implemented.
-   `utils/`: Includes utility functions that can be shared across the application, such as file handlers.

## Services

The backend is designed to be extensible with multiple image generation services. All services must implement the `BaseImageGenerationService` interface defined in `backend/services/base_service.py`.

### Current Services:

-   **GeminiService**: Interacts with the Google Gemini API to generate images from text prompts and optional input images.
-   **DalleService**: Interacts with the OpenAI DALL-E API to generate images from text prompts.

## API Endpoints

All API endpoints are defined under the `routes/` directory.

-   `POST /upload`: The primary endpoint for image generation.
    -   **Payload**: `prompt` (string), `file` (optional image), `model` (string).
    -   **Description**: Accepts a text prompt and an optional image, and uses the specified model to generate a new image.

## How to Add a New Service

1.  Create a new service class in the `services/` directory (e.g., `dalle_service.py`).
2.  Ensure the new class inherits from `BaseImageGenerationService` and implements the `generate_image` method.
3.  Add any necessary API keys or configurations to `config/settings.py`.
4.  Update the service factory in `routes` to include the new service so it can be selected via the `model` parameter.
