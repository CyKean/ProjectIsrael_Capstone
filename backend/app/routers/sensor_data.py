from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
import os
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from app.services.database import get_database
from bson import ObjectId

router = APIRouter(prefix="/api")

load_dotenv()

subscribers: List[asyncio.Queue] = []

# ESP32-1 (NPK Soil pH)
class NPKSoilPHData(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    soilPh: float
    device_id: str  # Added device_id field

# ESP32-2 (Moisture/Climate) - Updated to match ESP32 payload
class MoistureClimateData(BaseModel):
    soilMoisture: float
    temperature: float
    humidity: float
    device_id: str  # Added device_id field

# ESP32-3 (Water Level)
class WaterLevelData(BaseModel):
    waterLevel: float
    device_id: str  # Added device_id field

@router.post("/esp32-1")
async def receive_npk_soilph(data: NPKSoilPHData):
    raw_data = data.dict()
    device_id = raw_data.pop("device_id")  # Extract device_id

    message = {
        "type": "esp32-1",
        "data": raw_data,
        "device_id": device_id
    }

    print(f"📡 Received ESP32-1 Data from {device_id}:", raw_data)

    try:
        # ✅ Save to MongoDB collection "sensor_readings" with type "esp32-1"
        db = await get_database()
        collection = db["sensor_readings"]
        
        await collection.insert_one({
            **raw_data,
            "device_id": device_id,
            "sensor_type": "esp32-1",
            "timestamp": datetime.utcnow()
        })
        print(f"✅ ESP32-1 data saved to MongoDB for device {device_id}")
    except Exception as e:
        print(f"❌ MongoDB save error (ESP32-1): {e}")

    for queue in subscribers:
        await queue.put(message)

    return {"message": "ESP32-1 data received and broadcasted"}

# ========= ESP32-2 ROUTE ========== (Updated for ESP32-ENV)
@router.post("/esp32-2")
async def receive_moisture_temp_hum(data: MoistureClimateData):
    raw_data = data.dict()
    device_id = raw_data.pop("device_id")  # Extract device_id

    message = {
        "type": "esp32-2",
        "data": raw_data,
        "device_id": device_id
    }

    print(f"📡 Received ESP32-2 Data from {device_id}:", raw_data)

    try:
        # ✅ Save to MongoDB collection "sensor_readings" with type "esp32-2"
        db = await get_database()
        collection = db["sensor_readings"]
        
        await collection.insert_one({
            **raw_data,
            "device_id": device_id,
            "sensor_type": "esp32-2",
            "timestamp": datetime.utcnow()
        })
        print(f"✅ ESP32-2 data saved to MongoDB for device {device_id}")
    except Exception as e:
        print(f"❌ MongoDB save error (ESP32-2): {e}")

    for queue in subscribers:
        await queue.put(message)

    return {"message": "ESP32-2 data received and broadcasted"}

# ========= ESP32-3 ROUTE ==========
@router.post("/esp32-3")
async def receive_water_level(data: WaterLevelData):
    raw_data = data.dict()
    device_id = raw_data.pop("device_id")  # Extract device_id
    
    message = {
        "type": "esp32-3",
        "data": raw_data,
        "device_id": device_id
    }

    print(f"📡 Received ESP32-3 Water Level from {device_id}: {raw_data['waterLevel']}")

    try:
        # ✅ Save to MongoDB collection "water_level_readings"
        db = await get_database()
        collection = db["water_level_readings"]
        
        await collection.insert_one({
            **raw_data,
            "device_id": device_id,
            "timestamp": datetime.utcnow()
        })
        print(f"✅ Water level saved to MongoDB for device {device_id}")
    except Exception as e:
        print(f"❌ MongoDB save error (ESP32-3): {e}")

    for queue in subscribers:
        await queue.put(message)

    return {"message": "ESP32-3 data received and broadcasted"}

# ========= UNIFIED STREAM ==========
@router.get("/stream")
async def stream_sensor_data():
    queue = asyncio.Queue()
    subscribers.append(queue)

    async def event_generator():
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(jsonable_encoder(data))}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            subscribers.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# ========= GET HISTORICAL DATA ==========
@router.get("/sensor-readings")
async def get_sensor_readings(sensor_type: Optional[str] = None, device_id: Optional[str] = None, limit: int = 100):
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Build query filter
        query_filter = {}
        if sensor_type:
            query_filter["sensor_type"] = sensor_type
        if device_id:
            query_filter["device_id"] = device_id
        
        # Get readings sorted by timestamp descending
        cursor = collection.find(query_filter).sort("timestamp", -1).limit(limit)
        readings = []
        
        async for doc in cursor:
            # Convert ObjectId to string and format timestamp
            doc["_id"] = str(doc["_id"])
            doc["timestamp"] = doc["timestamp"].isoformat() if doc.get("timestamp") else None
            readings.append(doc)
        
        return {"readings": readings}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sensor readings: {str(e)}")

@router.get("/water-level-readings")
async def get_water_level_readings(device_id: Optional[str] = None, limit: int = 100):
    try:
        db = await get_database()
        collection = db["water_level_readings"]
        
        # Build query filter
        query_filter = {}
        if device_id:
            query_filter["device_id"] = device_id
        
        # Get readings sorted by timestamp descending
        cursor = collection.find(query_filter).sort("timestamp", -1).limit(limit)
        readings = []
        
        async for doc in cursor:
            # Convert ObjectId to string and format timestamp
            doc["_id"] = str(doc["_id"])
            doc["timestamp"] = doc["timestamp"].isoformat() if doc.get("timestamp") else None
            readings.append(doc)
        
        return {"readings": readings}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving water level readings: {str(e)}")