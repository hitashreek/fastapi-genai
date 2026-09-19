from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables

from routes.orders import router as orders_router
from routes.stats import router as stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created.")
    yield
    print("Application shutdown.")
    
    
app = FastAPI(
    title="Dabbe Wala Delivery API",
    description="API for managing deliveries, tracking order statuses and statistics for Dabbe Wala Delivery service.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(orders_router)
app.include_router(stats_router)


app.get("/health", tags=["health"])(lambda: {"status": "ok"})

