from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@router.get("/live")
async def liveness():
    return {"status": "alive"}

# TODO: Implement readiness check for database and other infrastructure dependencies
@router.get("/ready")
async def readiness():
    return {"status": "ready"}