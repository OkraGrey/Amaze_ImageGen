"""
API routes for image generation.
"""
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os

from backend.services.service_factory import get_service
from backend.utils.file_utils import save_uploaded_file, allowed_file
from backend.utils.prompting_utility import get_prompting_details
from backend.config.settings import BASE_DIR
# from backend.utils.bg_remover_op import remove_bg
from backend.utils.file_utils import remove_bg
router = APIRouter()

class DownloadRequest(BaseModel):
    path: str

@router.post("/upload")
async def upload_image(
    prompt: str = Form(...),
    file: Optional[UploadFile] = File(None),
    model: str = Form(...)
):
    print(f"[INFO]---INSIDE GENERATION ROUTES---")
    try:
        # Save uploaded file if provided
        
        file_path = None
        # img_details = None
        if file and file.filename:
            print(f"[INFO]---CHECKING IF FILE IS ALLOWED---")
            if not allowed_file(file.filename):
                raise HTTPException(status_code=400, detail="FILE TYPE NOT ALLOWED")

            file_path = save_uploaded_file(file)
            print(f"[INFO]---FILE SAVED SUCCESSFULLY---")
        #     img_details = get_prompting_details(file_path)
        #     improved_prompt = f"YOU ARE BEING PROVIDED WITH A USER QUERY AND A REFERENCE IMAGE AND A JSON DESCRIPTION THE IMAGE. **USER REQUIREMENTS ARE OF HIGHEST PRIORITY** . JSON DESCRIPTION IS GIVEN FOR MORE UNDERSTANDING OF THE PROVIDED IMAGE. CLUB THE PROVIDED KNOWLEDGE TO PRODUCE THE BEST POSSIBLE OUTPUT.\n # USER QUERY: {prompt} # \nIMG_DETAILS: {img_details}" 
        # # VALIDATE MODEL NAME TO MATCH WITH BACKEND
        # CREATE AN ENNUM TO TRACK THE MODEL NAME
        # IF THE MODEL NAME IS NOT IN THE ENUM, RAISE AN ERROR
        # IF THE MODEL NAME IS IN THE ENUM, GET THE SERVICE FROM THE FACTORY
        
        # Get the appropriate service from the factory
        print(f"[INFO]---GETTING SERVICE FROM THE FACTORY WITH MODEL NAME: {model}---")
        service = get_service(model)
        result_path = None
        result_filename = None
        
        if service:
            print(f"[INFO]---SERVICE FOUND IN THE FACTORY---",flush=True)
            result_path = service.generate_image(prompt, file_path)

            print(f"[INFO]---RESULT PATH RECIEVED FROM SERVICE: {result_path}---")
            result_filename = os.path.basename(result_path)
        
            return JSONResponse(content={
                "success": True,
                "message": "Image generated successfully",
                "result_path": f"/results/{result_filename}"
            })
        else:
            raise HTTPException(status_code=400, detail="SERVICE NOT FOUND")
    except ValueError as e:
        # Handle the case where the model is not supported
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download")
async def download_image(request: DownloadRequest):
    """
    Processes an image for download by removing its background using OpenAI GPT-image-1.

    Args:
        request: DownloadRequest containing the image path

    Returns:
        JSONResponse with the path to the processed image
    """
    print(f"[INFO]--- DOWNLOAD REQUEST RECEIVED ---")
    print(f"[INFO]--- Original path from request: {request.path} ---")

    try:
        # Extract filename from the URL path
        # The path comes as "/results/filename.png" or similar
        if request.path.startswith('/results/'):
            filename = request.path.replace('/results/', '')
        elif request.path.startswith('results/'):
            filename = request.path.replace('results/', '')
        else:
            # Extract just the filename from the path
            filename = os.path.basename(request.path)

        # Construct the full filesystem path
        image_path = os.path.join(BASE_DIR, 'results', filename)

        print(f"[INFO]--- Resolved filesystem path: {image_path} ---")

        # Verify the file exists
        if not os.path.exists(image_path):
            print(f"[ERROR]--- Image not found at path: {image_path} ---")
            raise HTTPException(status_code=404, detail=f"Image not found: {filename}")

        print(f"[INFO]--- Image file confirmed to exist ---")
        print(f"[INFO]--- Initiating background removal using OpenAI GPT-image-1 ---")

        # Remove background using OpenAI API
        processed_image_path_fs = remove_bg(image_path)
        # processed_image_path_fs= image_path

        print(f"[INFO]--- Background removal completed. Processed image saved at: {processed_image_path_fs} ---")

        # Convert filesystem path back to URL path
        # Get just the filename from the processed path
        processed_filename = os.path.basename(processed_image_path_fs)
        processed_image_path_url = f"/results/{processed_filename}"

        print(f"[INFO]--- Returning processed image URL: {processed_image_path_url} ---")

        return JSONResponse(content={
            "success": True,
            "message": "Background removed successfully. Image ready for download.",
            "path": processed_image_path_url
        })

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"[ERROR]--- Failed to process download request: {str(e)} ---")
        raise HTTPException(status_code=500, detail=str(e))
