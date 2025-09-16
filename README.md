# Image Generation Web App

## Overview
Web application for image generation using Google's Gemini API. Upload an image (optional), provide a text prompt, and get AI-generated images.

## Project Structure
- `frontend/`: UI components and static assets
- `backend/`: API server and Gemini integration
- `uploads/`: Directory for uploaded images
- `results/`: Directory for generated images

## Progress Tracker
- [x] Project setup and directory structure
- [x] Backend API development
  - [x] Gemini service integration
  - [x] Upload endpoint
  - [x] Result endpoint
- [x] Frontend development
  - [x] UI components
  - [x] Image upload functionality
  - [x] API integration
- [ ] Testing and refinement
- [ ] Deployment

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python with FastAPI
- AI: Google Gemini API

## Getting Started

### Prerequisites
- Python 3.9+
- Google Gemini API key

### Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment:
   - Windows: `env\Scripts\activate`
   - Unix/MacOS: `source env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application
1. Start the server: `python main.py`
2. Open your browser and navigate to `http://localhost:8000`

## Usage
1. Upload an image (optional)
2. Enter a text prompt describing what you want to generate
3. Click "Generate" and wait for the result
4. Download the generated image
