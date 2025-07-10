from fastapi import APIRouter, HTTPException
from app.models.config_models import ESP2Config
from app.services.esp2_service import configure_esp2

router = APIRouter(
    prefix="/api/esp2",
    tags=["ESP32-2 Configuration"],
    responses={404: {"description": "Not found"}}
)

@router.post("/configuration")
async def apply_esp2_configuration(config: ESP2Config):
    try:
        result = await configure_esp2(config)
        return {
            "status": "success",
            "message": "Configuration applied to ESP32-2",
            "device_response": result
        }
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"ESP32-2 device offline: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error configuring ESP32-2: {str(e)}"
        )