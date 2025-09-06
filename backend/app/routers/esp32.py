from fastapi import APIRouter, HTTPException, Depends
import httpx
from datetime import datetime
from typing import Optional, Dict, Any
import time

# Use your specific import
from app.services.database import get_database

# Create the router object
router = APIRouter(prefix="/api/esp32", tags=["esp32"])

@router.get("/test-connection")
async def test_esp32_connection(ip_address: str):
    """
    Test connection to an ESP32 device with better timeout handling
    """
    try:
        # Test connection to ESP32 - try common endpoints
        endpoints_to_try = [
            f"http://{ip_address}/",
            f"http://{ip_address}/info",
            f"http://{ip_address}/status"
        ]
        
        response_data = {
            "success": False,
            "ip_address": ip_address,
            "status": "unreachable",
            "response_time_ms": 0,
            "signal_strength": 0,
            "message": "Could not connect to any endpoint"
        }
        
        async with httpx.AsyncClient(timeout=3.0) as client:  # Reduced timeout to 3 seconds
            for endpoint in endpoints_to_try:
                try:
                    start_time = time.time()
                    response = await client.get(endpoint, timeout=2.0)  # Individual request timeout
                    response_time = (time.time() - start_time) * 1000
                    
                    if response.status_code == 200:
                        response_data = {
                            "success": True,
                            "ip_address": ip_address,
                            "status": "connected",
                            "response_time_ms": round(response_time, 2),
                            "signal_strength": 85,
                            "message": f"ESP32 is reachable at {endpoint}",
                            "firmware": "unknown"
                        }
                        
                        # Try to parse JSON response for more info
                        try:
                            json_data = response.json()
                            response_data.update({
                                "firmware": json_data.get("firmware", "unknown"),
                                "model": json_data.get("model", "ESP32"),
                                "version": json_data.get("version", "unknown")
                            })
                        except:
                            pass
                            
                        break
                        
                except httpx.ConnectError:
                    response_data["message"] = "Connection refused - device may be offline"
                    continue
                except httpx.TimeoutException:
                    response_data["message"] = f"Connection timeout to {endpoint}"
                    continue
                except Exception as e:
                    response_data["message"] = f"Error connecting: {str(e)}"
                    continue
        
        return response_data
                
    except Exception as e:
        # Provide more specific error information
        error_message = f"Connection test error: {str(e)}"
        if "timeout" in str(e).lower():
            error_message = "Connection timeout - device may be offline or unreachable"
        elif "connection" in str(e).lower():
            error_message = "Connection refused - device may be offline"
        
        raise HTTPException(status_code=500, detail=error_message)

@router.get("/device-info")
async def get_esp32_device_info(ip_address: str):
    """
    Get information from ESP32 device
    """
    try:
        # Try multiple common info endpoints
        info_endpoints = [
            f"http://{ip_address}/info",
            f"http://{ip_address}/api/info",
            f"http://{ip_address}/status",
            f"http://{ip_address}/api/status",
            f"http://{ip_address}/system/info"
        ]
        
        device_info = {
            "success": False,
            "ip_address": ip_address,
            "model": "ESP32",
            "firmware": "unknown",
            "mac": "unknown",
            "flash_size": "unknown",
            "free_heap": "unknown",
            "uptime": 0,
            "sensors": [],
            "sensor_readings": {},
            "last_contact": datetime.utcnow().isoformat()
        }
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            for endpoint in info_endpoints:
                try:
                    response = await client.get(endpoint)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        device_info = {
                            "success": True,
                            "ip_address": ip_address,
                            "model": data.get("model", "ESP32"),
                            "firmware": data.get("firmware", data.get("version", "unknown")),
                            "mac": data.get("mac", data.get("mac_address", "unknown")),
                            "flash_size": data.get("flash_size", data.get("flash", "unknown")),
                            "free_heap": data.get("free_heap", data.get("heap_free", "unknown")),
                            "uptime": data.get("uptime", data.get("running_time", 0)),
                            "sensors": data.get("sensors", data.get("connected_sensors", [])),
                            "sensor_readings": data.get("sensor_readings", data.get("readings", {})),
                            "last_contact": datetime.utcnow().isoformat(),
                            "raw_response": data  # Include raw response for debugging
                        }
                        break
                        
                except (httpx.ConnectError, httpx.TimeoutException):
                    continue  # Try next endpoint
                except Exception:
                    continue  # Try next endpoint
        
        # If no specific info endpoint worked, try basic ping
        if not device_info["success"]:
            # Test basic connectivity
            try:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    response = await client.get(f"http://{ip_address}/")
                    if response.status_code == 200:
                        device_info["success"] = True
                        device_info["message"] = "Device responsive but no info endpoint available"
            except:
                device_info["message"] = "Device not responsive"
        
        return device_info
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Device info error: {str(e)}")

@router.post("/ip")
async def save_esp32_ip(ip_data: dict, db = Depends(get_database)):
    """
    Save ESP32 IP address to database
    """
    try:
        ip_address = ip_data.get("ip")
        
        if not ip_address:
            raise HTTPException(status_code=400, detail="IP address is required")
        
        # Validate IP address format
        import re
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if not re.match(ip_pattern, ip_address):
            raise HTTPException(status_code=400, detail="Invalid IP address format")
        
        # Save to database
        collection = db["esp32_config"]
        result = collection.update_one(
            {"_id": "main_esp32"},
            {
                "$set": {
                    "ip_address": ip_address,
                    "updated_at": datetime.utcnow(),
                    "device_type": "esp32"
                }
            },
            upsert=True
        )
        
        return {
            "success": True,
            "message": "IP address saved successfully",
            "ip_address": ip_address,
            "modified_count": result.modified_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving IP: {str(e)}")

@router.get("/ip")
async def get_esp32_ip(db = Depends(get_database)):
    """
    Get saved ESP32 IP address
    """
    try:
        collection = db["esp32_config"]
        config = collection.find_one({"_id": "main_esp32"})
        
        if config and "ip_address" in config:
            return {
                "ip": config["ip_address"],
                "last_updated": config.get("updated_at"),
                "device_type": config.get("device_type", "esp32")
            }
        else:
            # Return default IP if none saved
            return {
                "ip": "192.168.1.14",
                "message": "Using default IP address",
                "is_default": True
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving IP: {str(e)}")

@router.get("/ping")
async def esp32_ping(ip_address: str):
    """
    Simple ping endpoint to check if ESP32 is alive
    """
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            start_time = time.time()
            response = await client.get(f"http://{ip_address}/")
            response_time = (time.time() - start_time) * 1000
            
            return {
                "success": response.status_code == 200,
                "ip_address": ip_address,
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "online": response.status_code == 200
            }
            
    except httpx.ConnectError:
        return {
            "success": False,
            "ip_address": ip_address,
            "online": False,
            "error": "Connection refused"
        }
    except httpx.TimeoutException:
        return {
            "success": False,
            "ip_address": ip_address,
            "online": False,
            "error": "Connection timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "ip_address": ip_address,
            "online": False,
            "error": str(e)
        }

@router.get("/scan")
async def scan_esp32_devices():
    """
    Scan for ESP32 devices on the network
    """
    try:
        # This is a placeholder - you might want to implement actual network scanning
        # or integrate with your network discovery service
        
        common_ips = [
            "192.168.1.14", "192.168.1.15", "192.168.1.16",
            "192.168.1.100", "192.168.1.101", "192.168.1.102",
            "192.168.0.100", "192.168.0.101", "192.168.0.102",
            "10.0.0.100", "10.0.0.101", "10.0.0.102"
        ]
        
        discovered_devices = []
        
        # Quick scan of common IPs
        async with httpx.AsyncClient(timeout=1.0) as client:
            for ip in common_ips:
                try:
                    response = await client.get(f"http://{ip}/", timeout=1.0)
                    if response.status_code == 200:
                        discovered_devices.append({
                            "ip": ip,
                            "online": True,
                            "status": "discovered"
                        })
                except:
                    continue
        
        return {
            "success": True,
            "discovered_devices": discovered_devices,
            "total_found": len(discovered_devices)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan error: {str(e)}")

# Export the router object for consistent import pattern
__all__ = ['router']