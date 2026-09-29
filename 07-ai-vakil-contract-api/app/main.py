from fastapi import FastAPI
from database import init_db
from routes.contracts import router as contract_router
from routes.analysis import router as analysis_router

app = FastAPI(
    title="Vakil Contract API",
    description="AI-Powered Contract Analysis using Gemini",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {    # a simple welcome/information endpoint.
        "app": "Vakeel Contracts API",
        "version": "1.0.0",
        "endpoints": {
            "POST /contracts/upload": "Upload a PDF or TXT contract for analysis",
            "GET /contracts/": "Retrieve a list of all uploaded contracts",
            "GET /contracts/{id}": "Retrieve details of a specific contract by ID",
            "POST /analysis/analyse/{contract_id}": "Analyze a contract using AI and return insights",
            "GET /analysis/{analysis_id}": "Retrieve the results of a specific analysis by ID",
            "GET /analysis/contract/{contract_id}": "Retrieve a list of all analysis performed for a specific contract",
        }
    }
    
app.include_router(contract_router)
app.include_router(analysis_router)
    
    