# dependencies.py
from fastapi import HTTPException, Depends
from app.services.database import get_database

async def get_esp32_ip():
    """Get ESP32 IP from MongoDB"""
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