from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import httpx

# Router configuration
router = APIRouter(
    prefix="/api/motor_status",
    tags=["Motor Status"]
)

# ESP32 Configuration
ESP32_IP = "http://192.168.1.14"   # Change this if your ESP32 has a new IP
ESP32_ENDPOINT = f"{ESP32_IP}/motor-status"

# Updated data model with source field
class MotorStatus(BaseModel):
    status: bool
    device_id: str
    user: str
    timestamp: datetime
    formatted_time: str
    source: str  # New field added here

# Route to handle motor toggle
@router.post("/")
async def save_motor_status(status_data: MotorStatus):
    print("✅ Received toggle from Vue frontend")
    print(f"Source: {status_data.source}")  # Log the source
    print(status_data.dict())

    payload = {
        "status": status_data.status,
        "source": status_data.source
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(ESP32_ENDPOINT, json=payload)
            response.raise_for_status()

        # ✅ SAFELY handle non-JSON responses
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