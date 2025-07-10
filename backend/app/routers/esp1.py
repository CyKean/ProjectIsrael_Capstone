from fastapi import APIRouter, HTTPException
from app.models.config_models import ESP1Config
from app.services.esp1_service import configure_esp1

router = APIRouter(
    prefix="/api/esp1",
    tags=["ESP32-1 Configuration"],
    responses={404: {"description": "Not found"}}
)

@router.post("/configuration")
async def apply_esp1_configuration(config: ESP1Config):
    try:
        result = await configure_esp1(config)
        return {
            "status": "success",
            "message": "Configuration applied to ESP32-1",
            "device_response": result
        }
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"ESP32-1 device offline: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error configuring ESP32-1: {str(e)}"
        )
