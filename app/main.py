from fastapi import FastAPI

from app.api.destinations import router as destinations_router
from app.api.dropoff_stops import router as dropoff_stops_router

app = FastAPI(
    title="DRT Route Assistant API",
    description="DRT 경로 안내 서비스 백엔드 API",
    version="0.1.0",
)


app.include_router(destinations_router)
app.include_router(dropoff_stops_router)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    return {
        "message": "DRT Route Assistant API",
    }


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
    }
