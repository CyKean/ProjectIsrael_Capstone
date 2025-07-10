from fastapi import APIRouter, HTTPException
from app.models.config_models import ESP3Config
from app.services.esp3_service import configure_esp3

router = APIRouter(
    prefix="/api/esp3",
    tags=["ESP32-3 Configuration"],
    responses={404: {"description": "Not found"}}
)

@router.post("/configuration")
async def apply_esp3_configuration(config: ESP3Config):
    try:
        result = await configure_esp3(config)
        return {
            "status": "success",
            "message": "Configuration applied to ESP32-3",
            "device_response": result
        }
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"ESP32-3 device offline: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error configuring ESP32-3: {str(e)}"
        )