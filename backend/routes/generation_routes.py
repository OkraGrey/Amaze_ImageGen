"""
API routes for image generation.
"""
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import os

from backend.services.service_factory import get_service
from backend.utils.file_utils import save_uploaded_file, allowed_file

router = APIRouter()

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
        if file and file.filename:
            print(f"[INFO]---CHECKING IF FILE IS ALLOWED---")
            if not allowed_file(file.filename):
                raise HTTPException(status_code=400, detail="FILE TYPE NOT ALLOWED")

            file_path = save_uploaded_file(file)
            print(f"[INFO]---FILE SAVED SUCCESSFULLY---")


        # VALIDATE MODEL NAME TO MATCH WITH BACKEND
        # CREATE AN ENNUM TO TRACK THE MODEL NAME
        # IF THE MODEL NAME IS NOT IN THE ENUM, RAISE AN ERROR
        # IF THE MODEL NAME IS IN THE ENUM, GET THE SERVICE FROM THE FACTORY
        
        # Get the appropriate service from the factory
        print(f"[INFO]---GETTING SERVICE FROM THE FACTORY WITH MODEL NAME: {model}---")
        service = get_service(model)
        result_path = None
        result_filename = None
        
        if service:
            print(f"[INFO]---SERVICE FOUND IN THE FACTORY---")
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
