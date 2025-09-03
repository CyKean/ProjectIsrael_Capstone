from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from app.services.database import get_database
from bson import ObjectId
import motor.motor_asyncio

router = APIRouter(prefix="/api", tags=["NPK Data"])

# Pydantic models
class NPKReadingResponse(BaseModel):
    id: str
    device_id: str
    nitrogen: float
    phosphorus: float
    potassium: float
    timestamp: datetime
    soilPh: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    moisture: Optional[float] = None

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

# Helper function to convert timestamp to milliseconds for accurate sorting
def get_timestamp_ms(timestamp_obj):
    """Convert various timestamp formats to milliseconds since epoch"""
    if isinstance(timestamp_obj, dict) and '_seconds' in timestamp_obj:
        # Firebase timestamp format: {_seconds: 123456789, _nanoseconds: 123000000}
        return timestamp_obj['_seconds'] * 1000 + timestamp_obj.get('_nanoseconds', 0) // 1000000
    elif isinstance(timestamp_obj, datetime):
        # Python datetime object
        return int(timestamp_obj.timestamp() * 1000)
    elif isinstance(timestamp_obj, (int, float)):
        # Already in milliseconds or seconds
        if timestamp_obj > 1e12:  # Likely milliseconds
            return int(timestamp_obj)
        else:  # Likely seconds
            return int(timestamp_obj * 1000)
    else:
        # Default to current time
        return int(datetime.now().timestamp() * 1000)

# Helper function to convert MongoDB reading to response model
def npk_reading_helper(reading, device_id) -> dict:
    # Convert timestamp to datetime and get milliseconds for sorting
    timestamp_obj = reading.get('timestamp')
    
    # Get timestamp in milliseconds for accurate sorting
    timestamp_ms = get_timestamp_ms(timestamp_obj)
    
    # Convert to datetime object for response
    if isinstance(timestamp_obj, dict) and '_seconds' in timestamp_obj:
        timestamp = datetime.fromtimestamp(timestamp_obj['_seconds'])
    elif isinstance(timestamp_obj, datetime):
        timestamp = timestamp_obj
    elif isinstance(timestamp_obj, (int, float)):
        # Convert from milliseconds or seconds to datetime
        if timestamp_obj > 1e12:  # Milliseconds
            timestamp = datetime.fromtimestamp(timestamp_obj / 1000)
        else:  # Seconds
            timestamp = datetime.fromtimestamp(timestamp_obj)
    else:
        timestamp = datetime.now()
    
    return {
        "id": str(reading.get("_id", ObjectId())),
        "device_id": device_id,
        "nitrogen": reading.get("nitrogen", 0),
        "phosphorus": reading.get("phosphorus", 0),
        "potassium": reading.get("potassium", 0),
        "soilPh": reading.get("soilPh"),
        "timestamp": timestamp,
        "timestamp_ms": timestamp_ms,  # For accurate sorting
        "temperature": reading.get("temperature"),
        "humidity": reading.get("humidity"),
        "moisture": reading.get("moisture")
    }

@router.get("/npk-data", response_model=List[NPKReadingResponse])
async def get_npk_data():
    """
    Get all NPK sensor readings from esp32-1 device, sorted by timestamp (newest first)
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Specifically get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
        readings = device.get("readings", [])
        all_readings = []
        
        # Process each reading from esp32-1
        for reading in readings:
            # Create response object
            response_reading = npk_reading_helper(reading, "esp32-1")
            all_readings.append(response_reading)
        
        # Sort by timestamp milliseconds descending (newest first) - MOST ACCURATE
        all_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Remove the temporary timestamp_ms field before returning
        for reading in all_readings:
            reading.pop('timestamp_ms', None)
        
        return all_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching NPK data: {str(e)}")

@router.get("/npk-data/recent", response_model=List[NPKReadingResponse])
async def get_recent_npk_data(
    hours: int = Query(1, ge=1, le=24),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get recent NPK sensor readings from esp32-1
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Calculate time threshold in milliseconds
        time_threshold_ms = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        
        # Get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
        readings = device.get("readings", [])
        recent_readings = []
        
        for reading in readings:
            response_reading = npk_reading_helper(reading, "esp32-1")
            
            # Check if reading is within time threshold using milliseconds
            if response_reading['timestamp_ms'] >= time_threshold_ms:
                recent_readings.append(response_reading)
        
        # Sort by timestamp milliseconds descending (newest first)
        recent_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        recent_readings = recent_readings[:limit]
        
        # Remove the temporary timestamp_ms field
        for reading in recent_readings:
            reading.pop('timestamp_ms', None)
        
        return recent_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent NPK data: {str(e)}")

@router.get("/npk-data/stats/summary")
async def get_npk_stats_summary(
    days: int = Query(7, ge=1, le=365)
):
    """
    Get summary statistics for NPK readings from esp32-1
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Calculate time threshold in milliseconds
        time_threshold_ms = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        # Get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
        readings = device.get("readings", [])
        all_nitrogen = []
        all_phosphorus = []
        all_potassium = []
        total_readings = 0
        
        for reading in readings:
            response_reading = npk_reading_helper(reading, "esp32-1")
            
            # Check if reading is within time threshold using milliseconds
            if response_reading['timestamp_ms'] >= time_threshold_ms:
                nitrogen = reading.get('nitrogen')
                phosphorus = reading.get('phosphorus')
                potassium = reading.get('potassium')
                
                # Only include valid numeric values
                if nitrogen is not None and not isinstance(nitrogen, str):
                    all_nitrogen.append(float(nitrogen))
                if phosphorus is not None and not isinstance(phosphorus, str):
                    all_phosphorus.append(float(phosphorus))
                if potassium is not None and not isinstance(potassium, str):
                    all_potassium.append(float(potassium))
                
                total_readings += 1
        
        if total_readings > 0:
            return {
                "total_readings": total_readings,
                "nitrogen": {
                    "average": round(sum(all_nitrogen) / len(all_nitrogen), 2) if all_nitrogen else 0,
                    "min": round(min(all_nitrogen), 2) if all_nitrogen else 0,
                    "max": round(max(all_nitrogen), 2) if all_nitrogen else 0
                },
                "phosphorus": {
                    "average": round(sum(all_phosphorus) / len(all_phosphorus), 2) if all_phosphorus else 0,
                    "min": round(min(all_phosphorus), 2) if all_phosphorus else 0,
                    "max": round(max(all_phosphorus), 2) if all_phosphorus else 0
                },
                "potassium": {
                    "average": round(sum(all_potassium) / len(all_potassium), 2) if all_potassium else 0,
                    "min": round(min(all_potassium), 2) if all_potassium else 0,
                    "max": round(max(all_potassium), 2) if all_potassium else 0
                }
            }
        else:
            return {
                "total_readings": 0,
                "nitrogen": {"average": 0, "min": 0, "max": 0},
                "phosphorus": {"average": 0, "min": 0, "max": 0},
                "potassium": {"average": 0, "min": 0, "max": 0}
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

@router.get("/npk-data/debug-sorted")
async def debug_sorted_data():
    """
    Debug endpoint to verify sorting order with timestamps
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            return {"error": "Device esp32-1 not found"}
        
        readings = device.get("readings", [])
        sorted_readings = []
        
        # Process readings with timestamps
        for reading in readings:
            response_reading = npk_reading_helper(reading, "esp32-1")
            sorted_readings.append(response_reading)
        
        # Sort by timestamp milliseconds (newest first)
        sorted_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Prepare debug info
        debug_info = {
            "total_readings": len(sorted_readings),
            "sorting_method": "timestamp_ms descending (newest first)",
            "newest_5_readings": [],
            "oldest_5_readings": []
        }
        
        # Newest 5 readings
        for i, reading in enumerate(sorted_readings[:5]):
            debug_info["newest_5_readings"].append({
                "position": i + 1,
                "id": reading['id'],
                "timestamp": reading['timestamp'].isoformat(),
                "timestamp_ms": reading['timestamp_ms'],
                "nitrogen": reading['nitrogen'],
                "phosphorus": reading['phosphorus'],
                "potassium": reading['potassium']
            })
        
        # Oldest 5 readings
        for i, reading in enumerate(sorted_readings[-5:]):
            debug_info["oldest_5_readings"].append({
                "position": len(sorted_readings) - 4 + i,
                "id": reading['id'],
                "timestamp": reading['timestamp'].isoformat(),
                "timestamp_ms": reading['timestamp_ms'],
                "nitrogen": reading['nitrogen'],
                "phosphorus": reading['phosphorus'],
                "potassium": reading['potassium']
            })
        
        return debug_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")

@router.get("/npk-data/debug")
async def debug_npk_data():
    """
    Debug endpoint to see database structure
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            return {"error": "Device esp32-1 not found"}
        
        debug_info = {
            "device_id": device["_id"],
            "total_readings": len(device.get("readings", [])),
            "sample_readings": []
        }
        
        # Sample readings with timestamp info
        for i, reading in enumerate(device.get("readings", [])[:3]):
            timestamp_ms = get_timestamp_ms(reading.get('timestamp'))
            debug_info["sample_readings"].append({
                "index": i,
                "has_id": "_id" in reading,
                "id_value": str(reading.get("_id", "MISSING")),
                "nitrogen": reading.get("nitrogen"),
                "phosphorus": reading.get("phosphorus"),
                "potassium": reading.get("potassium"),
                "timestamp_raw": reading.get("timestamp"),
                "timestamp_type": type(reading.get("timestamp")).__name__ if reading.get("timestamp") else "None",
                "timestamp_ms": timestamp_ms
            })
        
        return debug_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")

@router.get("/npk-data/devices/list")
async def get_devices_list():
    """
    Get list of all unique device IDs
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get all device documents and extract their _id fields
        devices_cursor = collection.find({}, {"_id": 1})
        devices = await devices_cursor.to_list(length=None)
        
        device_ids = [device["_id"] for device in devices]
        
        return {"devices": device_ids}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching devices: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = await get_database()
        # Try to ping the database
        await db.command('ping')
        
        # Also check if esp32-1 exists
        collection = db.sensor_readings
        device = await collection.find_one({"_id": "esp32-1"})
        
        return {
            "status": "healthy", 
            "database": "connected",
            "esp32-1_exists": device is not None,
            "esp32-1_readings": len(device.get("readings", [])) if device else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")