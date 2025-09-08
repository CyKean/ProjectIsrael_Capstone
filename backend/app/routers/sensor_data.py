from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
import os
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone, timedelta
from app.services.database import get_database
from bson import ObjectId

router = APIRouter(prefix="/api")

load_dotenv()

subscribers: List[asyncio.Queue] = []

# Get Philippine timezone (UTC+8)
PH_TIMEZONE = timezone(timedelta(hours=8))

def get_ph_time():
    """Get current datetime in Philippine timezone"""
    return datetime.now(PH_TIMEZONE)

def convert_to_firestore_timestamp(dt):
    """Convert datetime to Firestore-like timestamp format"""
    timestamp = dt.timestamp()
    seconds = int(timestamp)
    nanoseconds = int((timestamp - seconds) * 1e9)
    return {
        "_seconds": seconds,
        "_nanoseconds": nanoseconds
    }

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

async def save_sensor_reading(sensor_type: str, reading_data: dict):
    """Save sensor reading to the appropriate document with readings array"""
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Create a unique ID for the reading
        reading_id = str(ObjectId())
        
        # Prepare the reading document with Philippine time in Firestore format
        reading = {
            "_id": reading_id,
            "device_id": reading_data["device_id"],
            "timestamp": convert_to_firestore_timestamp(get_ph_time())  # Use Firestore format
        }
        
        # Add sensor-specific fields
        if sensor_type == "esp32-1":
            reading.update({
                "nitrogen": reading_data["nitrogen"],
                "phosphorus": reading_data["phosphorus"],
                "potassium": reading_data["potassium"],
                "soilPh": reading_data["soilPh"]
            })
        elif sensor_type == "esp32-2":
            reading.update({
                "soilMoisture": reading_data["soilMoisture"],
                "temperature": reading_data["temperature"],
                "humidity": reading_data["humidity"]
            })
        
        # Update the document for this sensor type, pushing the new reading to the readings array
        await collection.update_one(
            {"_id": sensor_type},
            {
                "$push": {
                    "readings": {
                        "$each": [reading],
                        "$sort": {"timestamp._seconds": -1},  # Sort by seconds
                        "$slice": 1000  # Limit array size to prevent excessive growth
                    }
                },
                "$setOnInsert": {"_id": sensor_type}  # Create document if it doesn't exist
            },
            upsert=True
        )
        
        print(f"✅ {sensor_type} data saved to MongoDB for device {reading_data['device_id']}")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB save error ({sensor_type}): {e}")
        return False

@router.post("/esp32-1")
async def receive_npk_soilph(data: NPKSoilPHData):
    raw_data = data.dict()
    device_id = raw_data.pop("device_id")  # Extract device_id

    message = {
        "type": "esp32-1",
        "data": raw_data,
        "device_id": device_id,
        "timestamp": convert_to_firestore_timestamp(get_ph_time())  # Add Firestore format timestamp
    }

    print(f"📡 Received ESP32-1 Data from {device_id}:", raw_data)

    # Save to MongoDB in the new format
    await save_sensor_reading("esp32-1", {"device_id": device_id, **raw_data})

    for queue in subscribers:
        await queue.put(message)

    return {"message": "ESP32-1 data received and broadcasted"}

@router.post("/esp32-2")
async def receive_moisture_temp_hum(data: MoistureClimateData):
    raw_data = data.dict()
    device_id = raw_data.pop("device_id")  # Extract device_id

    message = {
        "type": "esp32-2",
        "data": raw_data,
        "device_id": device_id,
        "timestamp": convert_to_firestore_timestamp(get_ph_time())  # Add Firestore format timestamp
    }

    print(f"📡 Received ESP32-2 Data from {device_id}:", raw_data)

    # Save to MongoDB in the new format
    await save_sensor_reading("esp32-2", {"device_id": device_id, **raw_data})

    for queue in subscribers:
        await queue.put(message)

    return {"message": "ESP32-2 data received and broadcasted"}

@router.post("/esp32-3")
async def receive_water_level(data: WaterLevelData):
    raw_data = data.dict()
    device_id = raw_data.pop("device_id")  # Extract device_id
    
    message = {
        "type": "esp32-3",
        "data": raw_data,
        "device_id": device_id,
        "timestamp": convert_to_firestore_timestamp(get_ph_time())  # Add Firestore format timestamp
    }

    print(f"📡 Received ESP32-3 Water Level from {device_id}: {raw_data['waterLevel']}")

    try:
        # ✅ Save to MongoDB collection "water_level_readings" with Firestore format timestamp
        db = await get_database()
        collection = db["water_level_readings"]
        
        await collection.insert_one({
            **raw_data,
            "device_id": device_id,
            "timestamp": convert_to_firestore_timestamp(get_ph_time())  # Use Firestore format
        })
        print(f"✅ Water level saved to MongoDB for device {device_id}")
    except Exception as e:
        print(f"❌ MongoDB save error (ESP32-3): {e}")

    for queue in subscribers:
        await queue.put(message)

    return {"message": "ESP32-3 data received and broadcasted"}

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

@router.get("/sensor-readings")
async def get_sensor_readings(sensor_type: Optional[str] = None, device_id: Optional[str] = None, limit: int = 100):
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Build query filter
        query_filter = {}
        if sensor_type:
            query_filter["_id"] = sensor_type
        
        # Get the sensor document
        sensor_doc = await collection.find_one(query_filter)
        
        if not sensor_doc:
            return {"readings": []}
        
        readings = sensor_doc.get("readings", [])
        
        # Filter by device_id if provided
        if device_id:
            readings = [reading for reading in readings if reading.get("device_id") == device_id]
        
        # Apply limit and ensure we have the most recent readings
        readings = readings[:limit]
        
        # Convert ObjectId to string for each reading
        for reading in readings:
            reading["_id"] = str(reading["_id"])
        
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
        
        # Get readings sorted by timestamp descending (using seconds field)
        cursor = collection.find(query_filter).sort("timestamp._seconds", -1).limit(limit)
        readings = []
        
        async for doc in cursor:
            # Convert ObjectId to string
            doc["_id"] = str(doc["_id"])
            readings.append(doc)
        
        return {"readings": readings}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving water level readings: {str(e)}")