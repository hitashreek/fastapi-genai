import uuid
from fastapi import APIRouter, File, HTTPException, UploadFile
import os
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, UPLOAD_DIR
from service.document_parser import extract_text
from models import Contract
from database import contracts_collection
from bson import ObjectId

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
    
    contract_data = Contract(  # Taking the extracted text (parsed_text) and putting it into your Pydantic Contract model.
        filename=unique_name,
        original_filename=file.filename,
        text_content=parsed_text["text"] if isinstance(parsed_text, dict) else parsed_text,
        page_count=(parsed_text["page_count"]),
        word_count=(parsed_text["word_count"]),
    #     page_count=(parsed_text["page_count"]) if isinstance(parsed_text, dict) else len(parsed_text.splitlines()),
    #     word_count=(parsed_text["word_count"]) if isinstance(parsed_text, dict) else len(parsed_text.split()),
    )
    
    doc = contract_data.model_dump()
    result = contracts_collection.insert_one(doc)  # This inserts the contract into database (mydb.contracts)
    contract_data.id = str(result.inserted_id)
    
    return {
        "message": "File uploaded and processed successfully",
        "contract": contract_data.model_dump(),
        "id": contract_data.id,
    }
    
@router.get("/")
async def list_contracts():
    """
    List all uploaded contracts.
    """
    contracts = []
    for doc in contracts_collection.find({}, {"text_content": 0}):  # "text_content": 0 is to remove the text_content from the response
        contract = Contract(**doc)  # MongoDB document → Pydantic Contract
        contract.id = str(doc["_id"])  # Convert MongoDB _id (ObjectId) to string and assign it to contract.id    
        contracts.append(contract.model_dump())  # Pydantic (contract) model → Python dictionary
    return {"contracts": contracts}

@router.get("/{contract_id}")
async def get_contract(contract_id: str):
    """
    Retrieve a specific contract by its ID.
    """
    doc = contracts_collection.find_one({"_id": ObjectId(contract_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    contract = Contract(**doc)
    contract.id = str(doc["_id"])
    return {"contract": contract.model_dump()}  
    