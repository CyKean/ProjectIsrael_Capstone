from fastapi import APIRouter, HTTPException, Request
from app.services.esp32_ip_manager import ip_manager

router = APIRouter(
    prefix="/api/esp32",
    tags=["ESP32 Management"]
)

@router.post("/ip")
async def set_esp32_ip(request: Request):
    try:
        body = await request.json()
        ip = body.get("ip")
        
        if not ip:
            raise HTTPException(
                status_code=400,
                detail="IP address is required in the request body"
            )
            
        if not ip_manager.is_valid_ip(ip):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid IP address format: {ip}. Expected format like 192.168.1.1"
            )
            
        ip_manager.set_ip(ip)
        return {
            "status": "success",
            "ip": ip,
            "message": "ESP32 IP address updated successfully"
        }
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format in request body"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/ip")
async def get_esp32_ip():
    return {
        "ip": ip_manager.get_ip(),
        "message": "Current ESP32 IP address"
    }