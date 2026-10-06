from fastapi import FastAPI
from app.routes.planner import router as planner_router

app = FastAPI(
    title="Yatra Planner API",
    description="Aggregate travel data from multiple sources to provide a single plan with SSE support",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {
        "app": "Yatra Planner API",
        "version": "1.0.0",
        "endpoints": {
            "POST /plan": "Create a travel plan (Aggregated)",
            "GET /plan/stream": "Stream a travel plan (SSE)",
            "GET /plan/cache-stats": "View cache statistics for travel plans",
            "DELETE /plan/cache": "Clear the cache for travel plans"
        }
    }
    
app.include_router(planner_router)