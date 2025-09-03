from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os
from app.services.database import get_database

router = APIRouter(prefix="/api/soil-ph", tags=["Soil pH"])

# Pydantic models for request/response
class SoilPhResponse(BaseModel):
    id: str
    timestamp: float
    date: str
    time: str
    deviceId: str
    soilPh: str
    phStatus: str
    nitrogen: Optional[str] = None
    phosphorus: Optional[str] = None
    potassium: Optional[str] = None

# Helper functions
def format_date(date):
    if not date:
        return '--'
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day = date.day
    month = months[date.month - 1]
    year = date.year
    return f"{month} {day:02d}, {year}"

def format_time(date):
    if not date:
        return '--'
    hours = date.hour
    minutes = date.minute
    seconds = date.second
    ampm = 'AM' if hours < 12 else 'PM'
    hours = hours % 12
    hours = 12 if hours == 0 else hours
    return f"{hours:02d}:{minutes:02d}:{seconds:02d} {ampm}"

def convert_firebase_timestamp(timestamp_dict):
    """Convert Firebase timestamp object to datetime"""
    if isinstance(timestamp_dict, dict) and '_seconds' in timestamp_dict:
        return datetime.fromtimestamp(timestamp_dict['_seconds'] + timestamp_dict.get('_nanoseconds', 0) / 1e9)
    return datetime.now()

def calculate_ph_status(ph_value):
    """Calculate pH status based on pH value"""
    if ph_value is None:
        return "UNKNOWN"
    ph_num = float(ph_value)
    if ph_num < 6.6:
        return "ACIDIC"
    elif 6.6 <= ph_num <= 7.3:
        return "NEUTRAL"
    else:
        return "ALKALINE"

# API endpoints
@router.get("/readings", response_model=List[SoilPhResponse])
async def get_soil_ph_readings():
    try:
        db = await get_database()
        # Get the esp32-1 document which contains the readings array
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return []
        
        # Process the readings array - filter for soil pH readings
        results = []
        for reading in doc["readings"]:
            if "soilPh" in reading and reading["soilPh"] is not None:
                timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                
                results.append({
                    "id": reading.get("_id", ""),
                    "timestamp": timestamp.timestamp(),
                    "date": format_date(timestamp),
                    "time": format_time(timestamp),
                    "deviceId": reading.get("device_id", "esp32-1"),
                    "soilPh": f"{reading.get('soilPh', 0):.1f}",
                    "phStatus": calculate_ph_status(reading.get('soilPh')),
                    "nitrogen": f"{reading.get('nitrogen', 0):.0f}" if reading.get('nitrogen') is not None else "--",
                    "phosphorus": f"{reading.get('phosphorus', 0):.0f}" if reading.get('phosphorus') is not None else "--",
                    "potassium": f"{reading.get('potassium', 0):.0f}" if reading.get('potassium') is not None else "--"
                })
        
        # Sort by timestamp descending
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching soil pH data: {str(e)}")

@router.get("/readings/realtime", response_model=List[SoilPhResponse])
async def get_realtime_soil_ph():
    try:
        db = await get_database()
        # Get the esp32-1 document
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return []
        
        # Get readings from the last 5 minutes
        five_minutes_ago = datetime.now().timestamp() - 300
        
        # Process recent readings
        results = []
        for reading in doc["readings"]:
            if "soilPh" in reading and reading["soilPh"] is not None:
                timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                
                if timestamp.timestamp() >= five_minutes_ago:
                    results.append({
                        "id": reading.get("_id", ""),
                        "timestamp": timestamp.timestamp(),
                        "date": format_date(timestamp),
                        "time": format_time(timestamp),
                        "deviceId": reading.get("device_id", "esp32-1"),
                        "soilPh": f"{reading.get('soilPh', 0):.1f}",
                        "phStatus": calculate_ph_status(reading.get('soilPh')),
                        "nitrogen": f"{reading.get('nitrogen', 0):.0f}" if reading.get('nitrogen') is not None else "--",
                        "phosphorus": f"{reading.get('phosphorus', 0):.0f}" if reading.get('phosphorus') is not None else "--",
                        "potassium": f"{reading.get('potassium', 0):.0f}" if reading.get('potassium') is not None else "--"
                    })
        
        # Sort by timestamp descending and limit to 20 most recent
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results[:20]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching real-time soil pH data: {str(e)}")

@router.get("/stats")
async def get_soil_ph_stats(hours: int = 24):
    try:
        db = await get_database()
        # Get the esp32-1 document
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return {"min": 0, "max": 0, "avg": 0, "count": 0}
        
        # Calculate time threshold
        time_threshold = datetime.now().timestamp() - (hours * 3600)
        
        # Extract soil pH values from recent readings
        soil_ph_values = []
        for reading in doc["readings"]:
            if "soilPh" in reading and reading["soilPh"] is not None:
                timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                if timestamp.timestamp() >= time_threshold:
                    soil_ph_values.append(float(reading["soilPh"]))
        
        if not soil_ph_values:
            return {"min": 0, "max": 0, "avg": 0, "count": 0}
        
        # Calculate statistics
        return {
            "min": min(soil_ph_values),
            "max": max(soil_ph_values),
            "avg": sum(soil_ph_values) / len(soil_ph_values),
            "count": len(soil_ph_values)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating soil pH statistics: {str(e)}")

@router.get("/search")
async def search_soil_ph(query: str, limit: int = 50):
    try:
        db = await get_database()
        # Get the esp32-1 document
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return []
        
        # Search through readings
        results = []
        for reading in doc["readings"]:
            if "soilPh" in reading and reading["soilPh"] is not None:
                # Check if query matches any field
                matches = any(
                    str(value).lower().find(query.lower()) != -1 
                    for key, value in reading.items() 
                    if key not in ['_id', 'timestamp', 'device_id'] and value is not None
                )
                
                if matches:
                    timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                    
                    results.append({
                        "id": reading.get("_id", ""),
                        "timestamp": timestamp.timestamp(),
                        "date": format_date(timestamp),
                        "time": format_time(timestamp),
                        "deviceId": reading.get("device_id", "esp32-1"),
                        "soilPh": f"{reading.get('soilPh', 0):.1f}",
                        "phStatus": calculate_ph_status(reading.get('soilPh')),
                        "nitrogen": f"{reading.get('nitrogen', 0):.0f}" if reading.get('nitrogen') is not None else "--",
                        "phosphorus": f"{reading.get('phosphorus', 0):.0f}" if reading.get('phosphorus') is not None else "--",
                        "potassium": f"{reading.get('potassium', 0):.0f}" if reading.get('potassium') is not None else "--"
                    })
        
        # Sort by timestamp descending and limit results
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching soil pH data: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = await get_database()
        # Try to access the collection
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        return {
            "status": "healthy",
            "message": "Soil pH API is working",
            "has_data": doc is not None and "readings" in doc
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Soil pH API connection failed"
        }