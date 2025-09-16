"""
API routes for image generation.
"""
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import os

from backend.services.gemini_service import GeminiService
from backend.utils.file_utils import save_uploaded_file, allowed_file

router = APIRouter()
gemini_service = GeminiService()

@router.post("/upload")
async def upload_image(
    prompt: str = Form(...),
    file: Optional[UploadFile] = File(None),
    model: str = Form(...)
):
    """
    Upload an image and a prompt for generation.
    
    Args:
        prompt (str): The text prompt for image generation
        file (UploadFile, optional): The image file to upload
        
    Returns:
        JSONResponse: The response containing the path to the generated image
    """
    try:
        # Save uploaded file if provided
        
        file_path = None
        if file and file.filename:
            if not allowed_file(file.filename):
                raise HTTPException(status_code=400, detail="File type not allowed")
            
            file_path = save_uploaded_file(file)
        
        # Generate image
        result_path = gemini_service.generate_image(prompt, file_path)
        
        # Get the filename only
        result_filename = os.path.basename(result_path)
        
        return JSONResponse(content={
            "success": True,
            "message": "Image generated successfully",
            "result_path": f"/results/{result_filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
