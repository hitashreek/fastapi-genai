from fastapi import APIRouter, UploadFile, File, HTTPException
from services.image import validate_image, resize_image_if_needed, save_image
import uuid
from services.vision import analyse_image as vision_analyse_image

router = APIRouter(
    prefix="/analyse",
    tags=["Analyse"]
)

async def process_single_image(file: UploadFile):
    """
    Process a single image for disease detection.
    """

    content = await file.read()

    validation = validate_image(content, file.content_type)
    if not validation["is_valid"]:
        raise HTTPException(status_code=400, detail=validation["message"])
    
    processed = resize_image_if_needed(content)

    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    path = save_image(processed, "uploads", unique_name)
    result = await vision_analyse_image(path, file.content_type)

    return result
    
   
@router.post("/")
async def analyse_image(file: UploadFile = File(...)):
    """
    Endpoint to upload an image for disease detection.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Here you would add the logic to process the uploaded image and perform disease detection.
    result = await process_single_image(file)
    
    # For demonstration purposes, we'll return a mock response.
    
    return {
        "filename": file.filename,
        "result": result,
        "content_type": file.content_type,
        "message": "Image received and processed for disease detection."
    }