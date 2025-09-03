from fastapi import APIRouter, HTTPException
from pymongo import DESCENDING
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os
from app.services.database import get_database

router = APIRouter(prefix="/api/soil-analysis", tags=["Soil Analysis"])

# Pydantic models for request/response
class ESP32Response(BaseModel):
    id: str
    timestamp: float
    date: str
    time: str
    deviceId: str
    nitrogen: Optional[str] = None
    phosphorus: Optional[str] = None
    potassium: Optional[str] = None
    ph: Optional[str] = None
    temperature: Optional[str] = None
    humidity: Optional[str] = None
    soilMoisture: Optional[str] = None

# Helper functions
def format_date(date):
    if not date:
        return '--'
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day = date.day
    month = months[date.month - 1]
    year = date.year
    return f"{month} {day}, {year}"

def format_time(date):
    if not date:
        return '--'
    hours = date.hour
    minutes = date.minute
    ampm = 'AM' if hours < 12 else 'PM'
    hours = hours % 12
    hours = 12 if hours == 0 else hours
    return f"{hours:02d}:{minutes:02d} {ampm}"

def convert_firebase_timestamp(timestamp_dict):
    """Convert Firebase timestamp object to datetime"""
    if isinstance(timestamp_dict, dict) and '_seconds' in timestamp_dict:
        return datetime.fromtimestamp(timestamp_dict['_seconds'] + timestamp_dict.get('_nanoseconds', 0) / 1e9)
    return datetime.now()

# API endpoints - fixed to match your database structure
@router.get("/esp32-1", response_model=List[ESP32Response])
async def get_esp32_1_data():
    try:
        db = await get_database()
        # Get the esp32-1 document which contains the readings array
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return []
        
        # Process the readings array
        results = []
        for reading in doc["readings"]:
            timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
            
            results.append({
                "id": reading.get("_id", ""),
                "timestamp": timestamp.timestamp(),
                "date": format_date(timestamp),
                "time": format_time(timestamp),
                "deviceId": reading.get("device_id", "esp32-1"),
                "nitrogen": f"{reading.get('nitrogen', 0):.2f}" if reading.get('nitrogen') is not None else "--",
                "phosphorus": f"{reading.get('phosphorus', 0):.2f}" if reading.get('phosphorus') is not None else "--",
                "potassium": f"{reading.get('potassium', 0):.2f}" if reading.get('potassium') is not None else "--",
                "ph": f"{reading.get('soilPh', 0):.2f}" if reading.get('soilPh') is not None else "--"
            })
        
        # Sort by timestamp descending
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ESP32-1 data: {str(e)}")

@router.get("/esp32-2", response_model=List[ESP32Response])
async def get_esp32_2_data():
    try:
        db = await get_database()
        # Get the esp32-2 document which contains the readings array
        doc = await db.sensor_readings.find_one({"_id": "esp32-2"})
        
        if not doc or "readings" not in doc:
            return []
        
        # Process the readings array
        results = []
        for reading in doc["readings"]:
            timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
            
            results.append({
                "id": reading.get("_id", ""),
                "timestamp": timestamp.timestamp(),
                "date": format_date(timestamp),
                "time": format_time(timestamp),
                "deviceId": reading.get("device_id", "esp32-2"),
                "temperature": f"{reading.get('temperature', 0):.2f}" if reading.get('temperature') is not None else "--",
                "humidity": f"{reading.get('humidity', 0):.2f}" if reading.get('humidity') is not None else "--",
                "soilMoisture": f"{reading.get('soilMoisture', 0):.2f}" if reading.get('soilMoisture') is not None else "--"
            })
        
        # Sort by timestamp descending
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ESP32-2 data: {str(e)}")

# Update global search to match new structure
@router.get("/global-search")
async def global_search(query: str):
    try:
        db = await get_database()
        results = []
        
        # Search both esp32-1 and esp32-2 documents
        for device_id in ["esp32-1", "esp32-2"]:
            doc = await db.sensor_readings.find_one({"_id": device_id})
            
            if not doc or "readings" not in doc:
                continue
            
            for reading in doc["readings"]:
                # Check if any field contains the query
                matches = any(
                    str(value).lower().find(query.lower()) != -1 
                    for key, value in reading.items() 
                    if key not in ['_id', 'timestamp', 'device_id'] and value is not None
                )
                
                if matches:
                    timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                    
                    device_data = {
                        "id": reading.get("_id", ""),
                        "timestamp": timestamp.timestamp(),
                        "date": format_date(timestamp),
                        "time": format_time(timestamp),
                        "deviceId": device_id
                    }
                    
                    if device_id == "esp32-1":
                        device_data.update({
                            "nitrogen": f"{reading.get('nitrogen', 0):.2f}" if reading.get('nitrogen') is not None else "--",
                            "phosphorus": f"{reading.get('phosphorus', 0):.2f}" if reading.get('phosphorus') is not None else "--",
                            "potassium": f"{reading.get('potassium', 0):.2f}" if reading.get('potassium') is not None else "--",
                            "ph": f"{reading.get('soilPh', 0):.2f}" if reading.get('soilPh') is not None else "--"
                        })
                    else:
                        device_data.update({
                            "temperature": f"{reading.get('temperature', 0):.2f}" if reading.get('temperature') is not None else "--",
                            "humidity": f"{reading.get('humidity', 0):.2f}" if reading.get('humidity') is not None else "--",
                            "soilMoisture": f"{reading.get('soilMoisture', 0):.2f}" if reading.get('soilMoisture') is not None else "--"
                        })
                    
                    results.append(device_data)
        
        # Sort by timestamp descending
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing global search: {str(e)}")