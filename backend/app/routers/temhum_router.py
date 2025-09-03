from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId
from app.services.database import get_database

router = APIRouter(prefix="/api/temperature-humidity", tags=["temperature-humidity"])

# Models
class Timestamp(BaseModel):
    _seconds: int
    _nanoseconds: int

class TemperatureHumidityReading(BaseModel):
    _id: Optional[str] = None
    device_id: Optional[str] = None  # Make device_id optional
    temperature: float
    humidity: float
    soilMoisture: Optional[int] = None
    timestamp: Timestamp

    class Config:
        schema_extra = {
            "example": {
                "device_id": "ESP32-ENV",
                "temperature": 29.2,
                "humidity": 78.8,
                "soilMoisture": 94,
                "timestamp": {
                    "_seconds": 1751511889,
                    "_nanoseconds": 235000000
                }
            }
        }

class ReadingStats(BaseModel):
    average: float
    min: float
    max: float

class StatsResponse(BaseModel):
    temperature: ReadingStats
    humidity: ReadingStats
    total_readings: int

@router.get("/readings", response_model=List[TemperatureHumidityReading])
async def get_temperature_humidity_readings(
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering"),
    db=Depends(get_database)
):
    """
    Get ALL temperature and humidity readings from esp32-2 document
    """
    try:
        # Get the esp32-2 document specifically
        document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
        if not document:
            return []
        
        # Get the readings array from the document
        readings_array = document.get("readings", [])
        
        # Apply date filtering if specified
        filtered_readings = []
        
        if start_date or end_date:
            start_seconds = int(start_date.timestamp()) if start_date else 0
            end_seconds = int(end_date.timestamp()) if end_date else float('inf')
            
            for reading in readings_array:
                timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
                if start_seconds <= timestamp_seconds <= end_seconds:
                    filtered_readings.append(reading)
        else:
            filtered_readings = readings_array
        
        # Sort by timestamp descending
        filtered_readings.sort(key=lambda x: x.get("timestamp", {}).get("_seconds", 0), reverse=True)
        
        # Convert ObjectId to string for JSON serialization
        for reading in filtered_readings:
            if "_id" in reading and isinstance(reading["_id"], ObjectId):
                reading["_id"] = str(reading["_id"])
        
        return filtered_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching readings: {str(e)}")

@router.get("/readings/recent", response_model=List[TemperatureHumidityReading])
async def get_recent_readings(
    hours: int = Query(24, description="Time window in hours for recent data"),
    db=Depends(get_database)
):
    """
    Get recent temperature and humidity readings from esp32-2 within specified time window
    """
    try:
        # Get the esp32-2 document specifically
        document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
        if not document:
            return []
        
        # Get the readings array from the document
        readings_array = document.get("readings", [])
        
        # Calculate time threshold
        time_threshold_seconds = int((datetime.utcnow() - timedelta(hours=hours)).timestamp())
        
        # Filter recent readings
        recent_readings = []
        for reading in readings_array:
            timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
            if timestamp_seconds >= time_threshold_seconds:
                recent_readings.append(reading)
        
        # Sort by timestamp descending
        recent_readings.sort(key=lambda x: x.get("timestamp", {}).get("_seconds", 0), reverse=True)
        
        # Convert ObjectId to string for JSON serialization
        for reading in recent_readings:
            if "_id" in reading and isinstance(reading["_id"], ObjectId):
                reading["_id"] = str(reading["_id"])
        
        return recent_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent readings: {str(e)}")

@router.get("/stats", response_model=StatsResponse)
async def get_temperature_humidity_stats(
    hours: Optional[int] = Query(None, description="Time window in hours for statistics"),
    start_date: Optional[datetime] = Query(None, description="Start date for statistics"),
    end_date: Optional[datetime] = Query(None, description="End date for statistics"),
    db=Depends(get_database)
):
    """
    Get statistics for temperature and humidity readings from esp32-2
    """
    try:
        # Get the esp32-2 document specifically
        document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
        if not document:
            return StatsResponse(
                temperature=ReadingStats(average=0, min=0, max=0),
                humidity=ReadingStats(average=0, min=0, max=0),
                total_readings=0
            )
        
        # Get the readings array from the document
        readings_array = document.get("readings", [])
        
        # Apply time filtering
        filtered_readings = []
        
        if hours:
            time_threshold_seconds = int((datetime.utcnow() - timedelta(hours=hours)).timestamp())
            for reading in readings_array:
                timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
                if timestamp_seconds >= time_threshold_seconds:
                    filtered_readings.append(reading)
        elif start_date or end_date:
            start_seconds = int(start_date.timestamp()) if start_date else 0
            end_seconds = int(end_date.timestamp()) if end_date else float('inf')
            for reading in readings_array:
                timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
                if start_seconds <= timestamp_seconds <= end_seconds:
                    filtered_readings.append(reading)
        else:
            filtered_readings = readings_array
        
        # Calculate statistics
        if filtered_readings:
            temperatures = [r.get("temperature", 0) for r in filtered_readings if r.get("temperature") is not None]
            humidities = [r.get("humidity", 0) for r in filtered_readings if r.get("humidity") is not None]
            
            if temperatures and humidities:
                return StatsResponse(
                    temperature=ReadingStats(
                        average=round(sum(temperatures) / len(temperatures), 2),
                        min=round(min(temperatures), 2),
                        max=round(max(temperatures), 2)
                    ),
                    humidity=ReadingStats(
                        average=round(sum(humidities) / len(humidities), 2),
                        min=round(min(humidities), 2),
                        max=round(max(humidities), 2)
                    ),
                    total_readings=len(filtered_readings)
                )
        
        return StatsResponse(
            temperature=ReadingStats(average=0, min=0, max=0),
            humidity=ReadingStats(average=0, min=0, max=0),
            total_readings=0
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

@router.get("/count")
async def get_readings_count(db=Depends(get_database)):
    """
    Get total count of temperature and humidity readings from esp32-2
    """
    try:
        # Get the esp32-2 document specifically
        document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
        if not document:
            return {"count": 0}
        
        # Get the readings array from the document
        readings_array = document.get("readings", [])
        
        count = len(readings_array)
        return {"count": count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting readings: {str(e)}")

@router.get("/test-document")
async def test_document(db=Depends(get_database)):
    """
    Test endpoint to check if esp32-2 document exists
    """
    try:
        # Get the esp32-2 document specifically
        document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
        if document:
            readings_count = len(document.get("readings", []))
            return {
                "exists": True,
                "readings_count": readings_count,
                "document_keys": list(document.keys())
            }
        else:
            # Check what documents exist
            collections = await db.list_collection_names()
            all_documents = await db["sensor_readings"].find().to_list(length=10)
            return {
                "exists": False,
                "collections": collections,
                "available_documents": [doc.get("_id", "unknown") for doc in all_documents]
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing document: {str(e)}")

# Make sure the router is exported
__all__ = ["router"]