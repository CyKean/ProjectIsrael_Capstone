from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime, timedelta
from typing import List, Optional, Any
from bson import ObjectId
from pydantic import BaseModel, Field

from app.services.database import get_database

router = APIRouter(prefix="/api/water-level", tags=["water-level"])

class WaterLevelReading(BaseModel):
    device_id: str = Field(..., description="Device identifier")
    waterLevel: float = Field(..., ge=0, le=100, description="Water level percentage")
    timestamp: Optional[datetime] = Field(None, description="Reading timestamp")

class WaterLevelResponse(BaseModel):
    id: str = Field(..., description="Document ID")
    device_id: str = Field(..., description="Device identifier")
    waterLevel: float = Field(..., ge=0, le=100, description="Water level percentage")
    timestamp: Optional[datetime] = Field(None, description="Reading timestamp")

class WaterLevelStats(BaseModel):
    min: float
    max: float
    avg: float
    count: int
    time_period_hours: int

def convert_firestore_timestamp(timestamp_data: Any) -> datetime:
    """Convert Firestore-style timestamp to Python datetime"""
    if isinstance(timestamp_data, datetime):
        return timestamp_data
    
    if isinstance(timestamp_data, dict):
        if '_seconds' in timestamp_data:
            # Firestore timestamp format
            seconds = timestamp_data['_seconds']
            nanoseconds = timestamp_data.get('_nanoseconds', 0)
            return datetime.fromtimestamp(seconds + nanoseconds / 1e9)
        elif 'seconds' in timestamp_data:
            # Alternative Firestore format
            seconds = timestamp_data['seconds']
            nanoseconds = timestamp_data.get('nanoseconds', 0)
            return datetime.fromtimestamp(seconds + nanoseconds / 1e9)
    
    # If it's already a string or other format, try to parse it
    try:
        return datetime.fromisoformat(str(timestamp_data))
    except (ValueError, TypeError):
        # Fallback to current time if parsing fails
        return datetime.now()

@router.get("/readings", response_model=List[WaterLevelResponse])
async def get_water_level_readings(
    skip: int = Query(0, ge=0),
    device_id: Optional[str] = None,
    db=Depends(get_database)
):
    """
    Get water level readings with optional filtering
    """
    try:
        query = {}
        if device_id:
            query["device_id"] = device_id
            
        # Remove the limit to fetch all data
        readings = await db["water_level_readings"].find(
            query, 
            sort=[("timestamp", -1)]
        ).skip(skip).to_list(length=None)  # length=None returns all documents
        
        # Convert the data to the expected format
        processed_readings = []
        for reading in readings:
            # Convert ObjectId to string
            reading_id = str(reading.get('_id', ''))
            
            # Convert Firestore timestamp to datetime
            timestamp = convert_firestore_timestamp(reading.get('timestamp'))
            
            processed_readings.append({
                "id": reading_id,
                "device_id": reading.get('device_id', ''),
                "waterLevel": reading.get('waterLevel', 0.0),
                "timestamp": timestamp
            })
        
        return processed_readings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching readings: {str(e)}")

@router.get("/readings/{reading_id}", response_model=WaterLevelResponse)
async def get_water_level_reading(reading_id: str, db=Depends(get_database)):
    """
    Get a specific water level reading by ID
    """
    try:
        if not ObjectId.is_valid(reading_id):
            raise HTTPException(status_code=400, detail="Invalid reading ID format")
            
        reading = await db["water_level_readings"].find_one({"_id": ObjectId(reading_id)})
        if not reading:
            raise HTTPException(status_code=404, detail="Reading not found")
        
        # Convert the data to the expected format
        timestamp = convert_firestore_timestamp(reading.get('timestamp'))
        
        return WaterLevelResponse(
            id=str(reading['_id']),
            device_id=reading.get('device_id', ''),
            waterLevel=reading.get('waterLevel', 0.0),
            timestamp=timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reading: {str(e)}")

@router.get("/latest", response_model=List[WaterLevelResponse])
async def get_latest_water_level_readings(
    limit: int = Query(10, ge=1, le=50),
    device_id: Optional[str] = None,
    db=Depends(get_database)
):
    """
    Get the latest water level readings
    """
    try:
        query = {}
        if device_id:
            query["device_id"] = device_id
            
        # Get readings from the last 5 minutes
        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        query["timestamp"] = {"$gte": five_minutes_ago}
        
        readings = await db["water_level_readings"].find(
            query, 
            sort=[("timestamp", -1)]
        ).limit(limit).to_list(length=limit)
        
        # Convert the data to the expected format
        processed_readings = []
        for reading in readings:
            # Convert ObjectId to string
            reading_id = str(reading.get('_id', ''))
            
            # Convert Firestore timestamp to datetime
            timestamp = convert_firestore_timestamp(reading.get('timestamp'))
            
            processed_readings.append({
                "id": reading_id,
                "device_id": reading.get('device_id', ''),
                "waterLevel": reading.get('waterLevel', 0.0),
                "timestamp": timestamp
            })
        
        return processed_readings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest readings: {str(e)}")

@router.post("/readings", response_model=WaterLevelResponse)
async def create_water_level_reading(reading: WaterLevelReading, db=Depends(get_database)):
    """
    Create a new water level reading
    """
    try:
        reading_dict = reading.dict()
        # Use provided timestamp or current time if not provided
        if not reading_dict.get("timestamp"):
            reading_dict["timestamp"] = datetime.now()
        
        result = await db["water_level_readings"].insert_one(reading_dict)
        created_reading = await db["water_level_readings"].find_one({"_id": result.inserted_id})
        
        # Convert the data to the expected format
        timestamp = convert_firestore_timestamp(created_reading.get('timestamp'))
        
        return WaterLevelResponse(
            id=str(created_reading['_id']),
            device_id=created_reading.get('device_id', ''),
            waterLevel=created_reading.get('waterLevel', 0.0),
            timestamp=timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating reading: {str(e)}")

@router.get("/stats", response_model=WaterLevelStats)
async def get_water_level_stats(
    device_id: Optional[str] = None,
    hours: int = Query(24, ge=1, le=168),  # Default to 24 hours, max 1 week
    db=Depends(get_database)
):
    """
    Get statistics for water level readings
    """
    try:
        query = {}
        if device_id:
            query["device_id"] = device_id
            
        # Get readings from the specified time period
        time_threshold = datetime.now() - timedelta(hours=hours)
        query["timestamp"] = {"$gte": time_threshold}
        
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "min": {"$min": "$waterLevel"},
                "max": {"$max": "$waterLevel"},
                "avg": {"$avg": "$waterLevel"},
                "count": {"$sum": 1}
            }}
        ]
        
        stats = await db["water_level_readings"].aggregate(pipeline).to_list(length=1)
        
        if stats and stats[0]:
            return WaterLevelStats(
                min=stats[0].get("min", 0),
                max=stats[0].get("max", 0),
                avg=stats[0].get("avg", 0),
                count=stats[0].get("count", 0),
                time_period_hours=hours
            )
        else:
            return WaterLevelStats(
                min=0,
                max=0,
                avg=0,
                count=0,
                time_period_hours=hours
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.get("/device/{device_id}/latest", response_model=WaterLevelResponse)
async def get_latest_reading_by_device(device_id: str, db=Depends(get_database)):
    """
    Get the latest reading for a specific device
    """
    try:
        reading = await db["water_level_readings"].find_one(
            {"device_id": device_id},
            sort=[("timestamp", -1)]
        )
        
        if not reading:
            raise HTTPException(status_code=404, detail="No readings found for this device")
        
        # Convert the data to the expected format
        timestamp = convert_firestore_timestamp(reading.get('timestamp'))
        
        return WaterLevelResponse(
            id=str(reading['_id']),
            device_id=reading.get('device_id', ''),
            waterLevel=reading.get('waterLevel', 0.0),
            timestamp=timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest reading: {str(e)}")