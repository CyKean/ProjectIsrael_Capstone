from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "ESP32 Configuration API"}