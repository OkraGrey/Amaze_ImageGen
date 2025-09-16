"""
Utility functions for file operations.
"""
import os
import uuid
from pathlib import Path
from backend.config.settings import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    
    Args:
        filename (str): The filename to check
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """
    Save an uploaded file to the upload directory.
    
    Args:
        file: The uploaded file object
        
    Returns:
        str: Path to the saved file
    """
    # Check file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File size exceeds the maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024)}MB")
    
    # Generate a unique filename
    original_filename = file.filename
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    filename = f"{uuid.uuid4().hex}.{extension}"
    
    # Save the file
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_path
