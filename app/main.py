from fastapi import FastAPI

app = FastAPI(
    title="DRT Route Assistant API",
    description="DRT 경로 안내 서비스 백엔드 API",
    version="0.1.0",
)


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
