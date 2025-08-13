import requests
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.schemas import ESP32IPRequest

router = APIRouter(prefix="/esp32", tags=["esp32"])

# In-memory storage
esp32_devices = {}

@router.post("/ip")
async def save_esp32_ip(request: ESP32IPRequest):
    """Save ESP32 IP address"""
    if not request.ip or len(request.ip.split('.')) != 4:
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    
    esp32_devices["last_known_ip"] = request.ip
    esp32_devices["last_contact"] = datetime.utcnow().isoformat()
    
    return {
        "message": f"ESP32 IP {request.ip} saved successfully",
        "saved_at": datetime.utcnow().isoformat()
    }

@router.get("/test-connection")
async def test_esp32_connection(ip_address: str):
    """Test connection to ESP32 device"""
    try:
        response = requests.get(f"http://{ip_address}/ping", timeout=3)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="ESP32 responded with error")
        
        data = response.json()
        esp32_devices["last_contact"] = datetime.utcnow().isoformat()
        esp32_devices["last_known_ip"] = ip_address
        
        return {
            "status": "connected",
            "ip_address": ip_address,
            "signal_strength": data.get("signalStrength", -70),
            "response_time_ms": response.elapsed.total_seconds() * 1000,
            "firmware": data.get("firmware", "unknown"),
            "last_contact": esp32_devices["last_contact"]
        }
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Connection to ESP32 timed out (3s)")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to ESP32")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/device-info")
async def get_esp32_device_info(ip_address: str):
    """Get detailed information about ESP32 device"""
    try:
        info_response = requests.get(f"http://{ip_address}/info", timeout=3)
        if info_response.status_code != 200:
            raise HTTPException(status_code=400, detail="ESP32 info endpoint failed")
        
        info_data = info_response.json()
        
        sensor_data = {}
        try:
            sensor_response = requests.get(f"http://{ip_address}/sensors", timeout=2)
            if sensor_response.status_code == 200:
                sensor_data = sensor_response.json()
        except:
            pass
        
        esp32_devices["last_contact"] = datetime.utcnow().isoformat()
        esp32_devices["last_known_ip"] = ip_address
        
        return {
            "model": info_data.get("model", "ESP32"),
            "firmware": info_data.get("firmware", "unknown"),
            "flash": info_data.get("flash", "4MB"),
            "mac": info_data.get("mac", "unknown"),
            "uptime": info_data.get("uptime", 0),
            "free_heap": info_data.get("heap", "unknown"),
            "sensors": info_data.get("sensors", []),
            "sensor_readings": sensor_data,
            "last_contact": esp32_devices["last_contact"],
            "ip_address": ip_address
        }
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Connection to ESP32 timed out (3s)")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to ESP32")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))