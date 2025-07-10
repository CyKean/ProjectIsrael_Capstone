from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
import os
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder

import firebase_admin
from firebase_admin import credentials, firestore

router = APIRouter(prefix="/api")

load_dotenv()

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
if not FIREBASE_CREDENTIALS:
    raise ValueError("Firebase credentials not found. Set FIREBASE_CREDENTIALS in .env")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

db = firestore.client()

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
        # ✅ Save to 3sensor_readings > esp32-1 > readings
        db.collection("3sensor_readings").document("esp32-1").collection("readings").add({
            **raw_data,
            "device_id": device_id,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ ESP32-1 data saved to Firebase for device {device_id}")
    except Exception as e:
        print(f"❌ Firebase save error (ESP32-1): {e}")

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
        # ✅ Save to 3sensor_readings > esp32-2 > readings
        db.collection("3sensor_readings").document("esp32-2").collection("readings").add({
            **raw_data,
            "device_id": device_id,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ ESP32-2 data saved to Firebase for device {device_id}")
    except Exception as e:
        print(f"❌ Firebase save error (ESP32-2): {e}")

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
        db.collection("water_level_readings").add({
            **raw_data,
            "device_id": device_id,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ Water level saved to Firebase for device {device_id}")
    except Exception as e:
        print(f"❌ Firebase save error (ESP32-3): {e}")

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