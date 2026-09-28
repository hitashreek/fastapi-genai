import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile
import os
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, UPLOAD_DIR
from service.document_parser import extract_text

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
)

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload a PDF or TXT contract for analysis
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    content = await file.read()
    
    size_mb = len(content) / (1024 * 1024)
    
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File size too large")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # exist_ok to avoid error if the folder already exists
    unique_name = f"{uuid.uuid4().hex}{ext}"
    
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    
    with open(file_path, "wb") as f:  # saving the file
        f.write(content)
        
    parsed_text = extract_text(file_path)