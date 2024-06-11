from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/liveness", include_in_schema=False)
async def liveness() -> str:
    return "OK"


@health_router.get("/readiness", include_in_schema=False)
async def readiness() -> str:
    return "OK"
