from fastapi import APIRouter, HTTPException, Request
from app.services.database import get_database

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
            
        if not is_valid_ip(ip):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid IP address format: {ip}. Expected format like 192.168.1.1"
            )
            
        # Save to MongoDB
        await save_ip_to_mongodb(ip)
        
        return {
            "status": "success",
            "ip": ip,
            "message": "ESP32 IP address updated successfully"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/ip")
async def get_esp32_ip():
    try:
        ip = await get_ip_from_mongodb()
        return {
            "ip": ip,
            "message": "Current ESP32 IP address"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving IP address: {str(e)}"
        )

def is_valid_ip(ip: str) -> bool:
    """Validate IP address format"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

async def save_ip_to_mongodb(ip: str):
    """Save IP address to MongoDB"""
    try:
        db = await get_database()
        collection = db.esp32_ip
        
        # Create collection if it doesn't exist (will be created automatically on first insert)
        
        # Upsert the IP address (there should only be one document)
        await collection.update_one(
            {"device": "esp32_main"},  # Filter
            {
                "$set": {
                    "ip": ip,
                    "last_updated": get_current_timestamp(),
                    "device": "esp32_main"
                }
            },
            upsert=True  # Create if doesn't exist
        )
        
    except Exception as e:
        raise Exception(f"Failed to save IP to database: {str(e)}")

async def get_ip_from_mongodb() -> str:
    """Get IP address from MongoDB"""
    try:
        db = await get_database()
        collection = db.esp32_ip
        
        # Find the IP document
        document = await collection.find_one({"device": "esp32_main"})
        
        if document and document.get("ip"):
            return document["ip"]
        else:
            # Return default IP if not found in database
            return "192.168.1.14"
            
    except Exception as e:
        print(f"Error retrieving IP from MongoDB: {e}")
        # Return default IP on error
        return "192.168.1.14"

def get_current_timestamp():
    """Get current timestamp in ISO format"""
    from datetime import datetime
    return datetime.now().isoformat()