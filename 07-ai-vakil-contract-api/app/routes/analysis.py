from fastapi import APIRouter, HTTPException
from config import GEMINI_API_KEY
from database import contracts_collection
from bson import ObjectId
from service.gemini_analyse import analyze_contract
from database import analysis_collection

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)


@router.post("/analyse/{contract_id}")
async def analyse_contract(contract_id: str):
    """
    Analyze a contract using AI and return insights.
    """

    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI API key is not configured")
    
    contract = contracts_collection.find_one({"_id": ObjectId(contract_id)})
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    if not contract.get("text_content"):
        raise HTTPException(status_code=400, detail="Contract has no text content to analyze")
    
    contracts_collection.update_one({"_id": ObjectId(contract_id)}, {"$set": {"analysis_status": "in_progress"}})

    result = await analyze_contract(contract_id, contract["text_content"])

    doc = result.model_dump()  
    insert_result = analysis_collection.insert_one(doc)  # This inserts the analysis into database (mydb.analysis)
    result.id = str(insert_result.inserted_id) # inserted_id is the ID that MongoDB generated for the document that was just inserted.

    contracts_collection.update_one({"_id": ObjectId(contract_id)}, {"$set": {"analysis_status": "completed"}})

    return {
        "message": "Contract analyzed successfully",
        "analysis": result.model_dump(),
        "id": result.id
    }


@router.get("/{analysis_id}")
def get_analysis(analysis_id: str):
    """
    Retrieve the results of a specific analysis by ID.
    """
    analysis = analysis_collection.find_one({"_id": ObjectId(analysis_id)})

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis["id"] = str(analysis.pop("_id"))  # "_id": ObjectId("6abb...") → remove _id & get ObjectId("6abb...") → convert to string "6abb..." → store as "id"
    return {
        "analysis": analysis
    }

@router.get('/')
def list_analyses():
    """
    List all analyses performed.
    """
    # _convert_obj() is both a helper because of its purpose, and recursive because of its behavior.
    def _convert_obj(obj):  # _convert_obj() is a helper function because it helps list_analyses() convert MongoDB data into JSON-friendly data.
       
        if isinstance(obj, list):  # isinstance means check what type something is - Is it a list?
            return [_convert_obj(v) for v in obj]  # Recursion means _convert_obj() call _convert_obj() on each element of the list
       
        if isinstance(obj, dict):  # Is it a dictionary? 
            new = {}
            for k, v in obj.items():  
                if k == '_id':
                    new['id'] = str(v)
                elif k != "id":                 
                    new[k] = _convert_obj(v)  # eg. new["contract_id"] = _convert_obj("6abadd79488600846f6044f0") It's not: list, dict, ObjectId, so it's a string
            return new
      
        if isinstance(obj, ObjectId):  # isinstance means check what type something is - Is it a ObjectId?
            return str(obj)
        
        return obj  # If it's not one of the above list, dict, ObjectId, so return it as it is.

    analyses = [_convert_obj(doc) for doc in analysis_collection.find({})]  # Get all MongoDB documents and convert each document.
    return {"analyses": analyses}


@router.get("/contract/{contract_id}")
async def get_analyses_for_contract(contract_id: str):
    """Get all analyses for a specific contract."""
    analyses = []
    cursor = analysis_collection.find({"contract_id": contract_id})

    for doc in cursor:
        doc["id"] = str(doc.pop("_id")) # "_id": ObjectId("6abb...") → remove _id & get ObjectId("6abb...") → convert to string "6abb..." → store as "id"
        analyses.append(doc)

    return {"analyses": analyses, "total": len(analyses)}