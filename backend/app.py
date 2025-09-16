"""
Main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from backend.routes.generation_routes import router as generation_router
from backend.config.settings import UPLOAD_DIR, RESULT_DIR

# Create FastAPI app
app = FastAPI(title="Image Generation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - removing the /api prefix since main.py already mounts this app at /api
app.include_router(generation_router, tags=["generation"])

# Mount static directories
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/results", StaticFiles(directory=RESULT_DIR), name="results")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Image Generation API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
