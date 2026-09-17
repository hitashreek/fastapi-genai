from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):  # Lifespan runs code during the application's startup and shutdown
    print("Lifespan started")
    # STARTUP: Create database tables when the app starts.
    create_tables()               
    print("Database tables created")
    
    # FastAPI runs the application while it is paused at this yield.
    yield  
    
    # SHUTDOWN: Code after yield every cleanup happen / runs when the app is shutting down.
    print("Shutting down the app")
        

# Create the FastAPI application.
app = FastAPI(
    title="Rangmanch Reviews API",
    description="Theatre reviews API for Pune Rangmanch",
    
    # Tell FastAPI to use our lifespan function.
    lifespan=lifespan
)


@app.get("/")
def root():
    return {"message": "Welcome to rangamanch review API"}

# This code uses FastAPI's lifespan to run code when the application starts and shuts down.