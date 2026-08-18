from fastapi import FastAPI

from src.api.routers.companies import router as companies_router
from src.api.routers.ratios import router as ratios_router

app = FastAPI(
    title="N100 Financial Intelligence API",
    description="API for the N100 Financial Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "N100 Financial Intelligence API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(companies_router)
app.include_router(ratios_router)