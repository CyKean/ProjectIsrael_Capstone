from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import httpx
from dependencies import get_esp32_ip 

# Router configuration
router = APIRouter(
    prefix="/api/motor_status",
    tags=["Motor Status"]
)

# ESP32 Configuration - Removed Depends from here since it can't be used at module level
# We'll use it inside the route function

class MotorStatus(BaseModel):
    status: bool
    device_id: str
    user: str
    timestamp: datetime
    formatted_time: str
    source: str

@router.post("/")
async def save_motor_status(
    status_data: MotorStatus,
    esp_ip: str = Depends(get_esp32_ip)  # Moved Depends here
):
    print(f"🔧 DEBUG: Using ESP32 IP from dependency: {esp_ip}")
    print("✅ Received toggle from Vue frontend")
    print(f"Source: {status_data.source}")
    print(status_data.dict())

    # Construct the endpoint with the actual IP
    esp32_endpoint = f"http://{esp_ip}/motor-status"

    payload = {
        "status": status_data.status,
        "source": status_data.source
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(esp32_endpoint, json=payload)
            response.raise_for_status()

        try:
            esp32_data = response.json()
        except ValueError:
            esp32_data = response.text

        print("✅ Successfully forwarded to ESP32.")
        return {
            "message": "Motor status received and forwarded",
            "esp32_response": esp32_data,
            "source": status_data.source
        }

    except httpx.RequestError as e:
        print(f"❌ Network error: {e}")
        raise HTTPException(status_code=500, detail=f"Network error: {e}")

    except httpx.HTTPStatusError as e:
        print(f"❌ ESP32 responded with HTTP {e.response.status_code}")
        print("📩 ESP32 response body:", e.response.text)
        raise HTTPException(status_code=500, detail=f"ESP32 error: {e.response.text}")