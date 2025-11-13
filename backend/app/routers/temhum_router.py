# from fastapi import APIRouter, HTTPException, Query, Depends
# from datetime import datetime, timedelta
# from typing import List, Optional
# from pydantic import BaseModel
# from bson import ObjectId
# from app.services.database import get_database

# router = APIRouter(prefix="/api/temperature-humidity", tags=["temperature-humidity"])

# # Models
# class Timestamp(BaseModel):
#     _seconds: int
#     _nanoseconds: int

# class TemperatureHumidityReading(BaseModel):
#     _id: Optional[str] = None
#     device_id: Optional[str] = None
#     temperature: float
#     humidity: float
#     soilMoisture: Optional[int] = None
#     timestamp: Timestamp

# class ReadingStats(BaseModel):
#     average: float
#     min: float
#     max: float

# class StatsResponse(BaseModel):
#     temperature: ReadingStats
#     humidity: ReadingStats
#     total_readings: int

# @router.get("/readings")
# async def get_temperature_humidity_readings(
#     start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
#     end_date: Optional[datetime] = Query(None, description="End date for filtering"),
#     db=Depends(get_database)
# ):
#     """
#     Get ALL temperature and humidity readings from esp32-2 document
#     """
#     try:
#         # Get the esp32-2 document specifically
#         document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
#         if not document:
#             print("Document esp32-2 not found in sensor_readings collection")
#             return []
        
#         # Get the readings array from the document
#         readings_array = document.get("readings", [])
#         print(f"Found {len(readings_array)} readings in esp32-2 document")
        
#         # Apply date filtering if specified
#         filtered_readings = []
        
#         if start_date or end_date:
#             start_seconds = int(start_date.timestamp()) if start_date else 0
#             end_seconds = int(end_date.timestamp()) if end_date else float('inf')
            
#             for reading in readings_array:
#                 timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
#                 if start_seconds <= timestamp_seconds <= end_seconds:
#                     filtered_readings.append(reading)
#         else:
#             filtered_readings = readings_array
        
#         # Sort by timestamp descending (newest first)
#         filtered_readings.sort(key=lambda x: x.get("timestamp", {}).get("_seconds", 0), reverse=True)
        
#         # Convert ObjectId to string for JSON serialization and ensure data types
#         processed_readings = []
#         for reading in filtered_readings:
#             processed_reading = reading.copy()
            
#             # Convert ObjectId to string
#             if "_id" in processed_reading and isinstance(processed_reading["_id"], ObjectId):
#                 processed_reading["_id"] = str(processed_reading["_id"])
            
#             # Ensure numeric values are properly typed
#             if "temperature" in processed_reading:
#                 processed_reading["temperature"] = float(processed_reading["temperature"])
#             if "humidity" in processed_reading:
#                 processed_reading["humidity"] = float(processed_reading["humidity"])
#             if "soilMoisture" in processed_reading:
#                 processed_reading["soilMoisture"] = int(processed_reading["soilMoisture"])
            
#             processed_readings.append(processed_reading)
        
#         print(f"Returning {len(processed_readings)} processed readings")
#         return processed_readings
        
#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         print(f"Error fetching readings: {str(e)}\n{error_details}")
#         raise HTTPException(status_code=500, detail=f"Error fetching readings: {str(e)}")

# @router.get("/readings/recent")
# async def get_recent_readings(
#     hours: int = Query(24, description="Time window in hours for recent data"),
#     db=Depends(get_database)
# ):
#     """
#     Get recent temperature and humidity readings from esp32-2 within specified time window
#     """
#     try:
#         # Get the esp32-2 document specifically
#         document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
#         if not document:
#             return []
        
#         # Get the readings array from the document
#         readings_array = document.get("readings", [])
        
#         # Calculate time threshold
#         time_threshold_seconds = int((datetime.utcnow() - timedelta(hours=hours)).timestamp())
        
#         # Filter recent readings
#         recent_readings = []
#         for reading in readings_array:
#             timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
#             if timestamp_seconds >= time_threshold_seconds:
#                 recent_readings.append(reading)
        
#         # Sort by timestamp descending
#         recent_readings.sort(key=lambda x: x.get("timestamp", {}).get("_seconds", 0), reverse=True)
        
#         # Convert ObjectId to string for JSON serialization
#         processed_readings = []
#         for reading in recent_readings:
#             processed_reading = reading.copy()
            
#             if "_id" in processed_reading and isinstance(processed_reading["_id"], ObjectId):
#                 processed_reading["_id"] = str(processed_reading["_id"])
            
#             # Ensure numeric values are properly typed
#             if "temperature" in processed_reading:
#                 processed_reading["temperature"] = float(processed_reading["temperature"])
#             if "humidity" in processed_reading:
#                 processed_reading["humidity"] = float(processed_reading["humidity"])
            
#             processed_readings.append(processed_reading)
        
#         return processed_readings
        
#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         print(f"Error fetching recent readings: {str(e)}\n{error_details}")
#         raise HTTPException(status_code=500, detail=f"Error fetching recent readings: {str(e)}")

# @router.get("/stats", response_model=StatsResponse)
# async def get_temperature_humidity_stats(
#     hours: Optional[int] = Query(None, description="Time window in hours for statistics"),
#     start_date: Optional[datetime] = Query(None, description="Start date for statistics"),
#     end_date: Optional[datetime] = Query(None, description="End date for statistics"),
#     db=Depends(get_database)
# ):
#     """
#     Get statistics for temperature and humidity readings from esp32-2
#     """
#     try:
#         # Get the esp32-2 document specifically
#         document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
#         if not document:
#             return StatsResponse(
#                 temperature=ReadingStats(average=0, min=0, max=0),
#                 humidity=ReadingStats(average=0, min=0, max=0),
#                 total_readings=0
#             )
        
#         # Get the readings array from the document
#         readings_array = document.get("readings", [])
        
#         # Apply time filtering
#         filtered_readings = []
        
#         if hours:
#             time_threshold_seconds = int((datetime.utcnow() - timedelta(hours=hours)).timestamp())
#             for reading in readings_array:
#                 timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
#                 if timestamp_seconds >= time_threshold_seconds:
#                     filtered_readings.append(reading)
#         elif start_date or end_date:
#             start_seconds = int(start_date.timestamp()) if start_date else 0
#             end_seconds = int(end_date.timestamp()) if end_date else float('inf')
#             for reading in readings_array:
#                 timestamp_seconds = reading.get("timestamp", {}).get("_seconds", 0)
#                 if start_seconds <= timestamp_seconds <= end_seconds:
#                     filtered_readings.append(reading)
#         else:
#             filtered_readings = readings_array
        
#         # Calculate statistics with proper data validation
#         temperatures = []
#         humidities = []
        
#         for reading in filtered_readings:
#             temp = reading.get("temperature")
#             humidity = reading.get("humidity")
            
#             # Validate and convert temperature
#             if temp is not None:
#                 try:
#                     temperatures.append(float(temp))
#                 except (ValueError, TypeError):
#                     pass
            
#             # Validate and convert humidity
#             if humidity is not None:
#                 try:
#                     humidities.append(float(humidity))
#                 except (ValueError, TypeError):
#                     pass
        
#         # Calculate statistics only if we have valid data
#         if temperatures and humidities:
#             return StatsResponse(
#                 temperature=ReadingStats(
#                     average=round(sum(temperatures) / len(temperatures), 2),
#                     min=round(min(temperatures), 2),
#                     max=round(max(temperatures), 2)
#                 ),
#                 humidity=ReadingStats(
#                     average=round(sum(humidities) / len(humidities), 2),
#                     min=round(min(humidities), 2),
#                     max=round(max(humidities), 2)
#                 ),
#                 total_readings=len(filtered_readings)
#             )
        
#         return StatsResponse(
#             temperature=ReadingStats(average=0, min=0, max=0),
#             humidity=ReadingStats(average=0, min=0, max=0),
#             total_readings=0
#         )
            
#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         print(f"Error calculating statistics: {str(e)}\n{error_details}")
#         raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

# @router.get("/count")
# async def get_readings_count(db=Depends(get_database)):
#     """
#     Get total count of temperature and humidity readings from esp32-2
#     """
#     try:
#         # Get the esp32-2 document specifically
#         document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
#         if not document:
#             return {"count": 0}
        
#         # Get the readings array from the document
#         readings_array = document.get("readings", [])
        
#         count = len(readings_array)
#         return {"count": count}
        
#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         print(f"Error counting readings: {str(e)}\n{error_details}")
#         raise HTTPException(status_code=500, detail=f"Error counting readings: {str(e)}")

# @router.get("/test-document")
# async def test_document(db=Depends(get_database)):
#     """
#     Test endpoint to check if esp32-2 document exists and examine its structure
#     """
#     try:
#         # Get the esp32-2 document specifically
#         document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
        
#         if document:
#             readings_count = len(document.get("readings", []))
            
#             # Sample a few readings to examine structure
#             sample_readings = []
#             if readings_count > 0:
#                 sample_readings = document.get("readings", [])[:3]  # First 3 readings
            
#             return {
#                 "exists": True,
#                 "readings_count": readings_count,
#                 "document_keys": list(document.keys()),
#                 "sample_readings": sample_readings
#             }
#         else:
#             # Check what documents exist
#             collections = await db.list_collection_names()
#             all_documents = await db["sensor_readings"].find().to_list(length=10)
#             return {
#                 "exists": False,
#                 "collections": collections,
#                 "available_documents": [doc.get("_id", "unknown") for doc in all_documents]
#             }
        
#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         print(f"Error testing document: {str(e)}\n{error_details}")
#         raise HTTPException(status_code=500, detail=f"Error testing document: {str(e)}")


# @router.get("/readings/raw")
# async def get_raw_readings_sample(limit: int = 5, db=Depends(get_database)):
#     """
#     Return a raw sample (first `limit`) of readings from esp32-2 without any processing.
#     Useful for debugging timestamp shapes and payload structure.
#     """
#     try:
#         document = await db["sensor_readings"].find_one({"_id": "esp32-2"})
#         if not document:
#             # return available document ids to help debug
#             all_docs = await db["sensor_readings"].find().to_list(length=20)
#             return {"exists": False, "available_documents": [d.get("_id") for d in all_docs]}

#         readings = document.get("readings", [])
#         # return raw slice
#         return {"count": len(readings), "sample": readings[:limit]}

#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         print(f"Error returning raw readings sample: {str(e)}\n{error_details}")
#         raise HTTPException(status_code=500, detail=f"Error returning raw readings sample: {str(e)}")

# # Make sure the router is exported
# __all__ = ["router"]

from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId
from app.services.database import get_database

router = APIRouter(prefix="/api/temperature-humidity", tags=["temperature-humidity"])

# Pydantic models
class TemperatureHumidityReadingResponse(BaseModel):
    id: str
    device_id: str
    temperature: float
    humidity: float
    timestamp: datetime
    soilMoisture: Optional[float] = None

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class ReadingStats(BaseModel):
    average: float
    min: float
    max: float

class StatsResponse(BaseModel):
    temperature: ReadingStats
    humidity: ReadingStats
    total_readings: int

class PaginatedResponse(BaseModel):
    data: List[TemperatureHumidityReadingResponse]
    pagination: dict

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
def temp_humidity_reading_helper(reading, device_id, index=None) -> dict:
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
    
    # Generate a unique ID for each reading
    reading_id = f"{device_id}_{timestamp_ms}"
    if index is not None:
        reading_id = f"{device_id}_{index}"
    
    return {
        "id": reading_id,
        "device_id": device_id,
        "temperature": reading.get("temperature", 0),
        "humidity": reading.get("humidity", 0),
        "soilMoisture": reading.get("soilMoisture"),
        "timestamp": timestamp,
        "timestamp_ms": timestamp_ms,  # For accurate sorting
    }

@router.get("/readings", response_model=PaginatedResponse)
async def get_temperature_humidity_readings(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query for device_id"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering")
):
    """
    Get paginated temperature and humidity readings from esp32-2 device, sorted by timestamp (newest first)
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Specifically get the esp32-2 device
        device = await collection.find_one({"_id": "esp32-2"})
        
        if not device:
            return {
                "data": [],
                "pagination": {
                    "currentPage": page,
                    "totalPages": 0,
                    "totalItems": 0,
                    "itemsPerPage": limit,
                    "hasNext": False,
                    "hasPrev": False
                }
            }
        
        readings = device.get("readings", [])
        all_readings = []
        
        # Process each reading from esp32-2
        for i, reading in enumerate(readings):
            # Create response object
            response_reading = temp_humidity_reading_helper(reading, "esp32-2", i)
            all_readings.append(response_reading)
        
        # Apply date filtering if specified
        filtered_readings = []
        
        if start_date or end_date:
            start_ms = int(start_date.timestamp() * 1000) if start_date else 0
            end_ms = int(end_date.timestamp() * 1000) if end_date else float('inf')
            
            for reading in all_readings:
                if start_ms <= reading['timestamp_ms'] <= end_ms:
                    filtered_readings.append(reading)
        else:
            filtered_readings = all_readings
        
        # Apply search filtering if specified
        if search:
            search_lower = search.lower()
            filtered_readings = [
                reading for reading in filtered_readings
                if reading.get("device_id", "").lower().find(search_lower) != -1
            ]
        
        # Sort by timestamp milliseconds descending (newest first)
        filtered_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Calculate pagination
        total_items = len(filtered_readings)
        total_pages = (total_items + limit - 1) // limit  # Ceiling division
        skip = (page - 1) * limit
        
        # Apply pagination
        paginated_readings = filtered_readings[skip:skip + limit]
        
        # Remove the temporary timestamp_ms field before returning
        for reading in paginated_readings:
            reading.pop('timestamp_ms', None)
        
        return {
            "data": paginated_readings,
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalItems": total_items,
                "itemsPerPage": limit,
                "hasNext": page < total_pages,
                "hasPrev": page > 1
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching temperature humidity data: {str(e)}")

@router.get("/readings/all", response_model=List[TemperatureHumidityReadingResponse])
async def get_all_temperature_humidity_readings(
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering")
):
    """
    Get ALL temperature and humidity readings (use with caution for large datasets)
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get the esp32-2 device
        device = await collection.find_one({"_id": "esp32-2"})
        
        if not device:
            return []
        
        readings = device.get("readings", [])
        all_readings = []
        
        for i, reading in enumerate(readings):
            response_reading = temp_humidity_reading_helper(reading, "esp32-2", i)
            all_readings.append(response_reading)
        
        # Apply date filtering if specified
        filtered_readings = []
        
        if start_date or end_date:
            start_ms = int(start_date.timestamp() * 1000) if start_date else 0
            end_ms = int(end_date.timestamp() * 1000) if end_date else float('inf')
            
            for reading in all_readings:
                if start_ms <= reading['timestamp_ms'] <= end_ms:
                    filtered_readings.append(reading)
        else:
            filtered_readings = all_readings
        
        # Sort by timestamp milliseconds descending (newest first)
        filtered_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Remove timestamp_ms field
        for reading in filtered_readings:
            reading.pop('timestamp_ms', None)
        
        return filtered_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all temperature humidity data: {str(e)}")

@router.get("/readings/recent", response_model=PaginatedResponse)
async def get_recent_temperature_humidity_readings(
    hours: int = Query(24, ge=1, le=168),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get recent temperature and humidity readings from esp32-2 with pagination
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Calculate time threshold in milliseconds
        time_threshold_ms = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        
        # Get the esp32-2 device
        device = await collection.find_one({"_id": "esp32-2"})
        
        if not device:
            return {
                "data": [],
                "pagination": {
                    "currentPage": page,
                    "totalPages": 0,
                    "totalItems": 0,
                    "itemsPerPage": limit,
                    "hasNext": False,
                    "hasPrev": False,
                    "timeframe_hours": hours
                }
            }
        
        readings = device.get("readings", [])
        recent_readings = []
        
        for i, reading in enumerate(readings):
            response_reading = temp_humidity_reading_helper(reading, "esp32-2", i)
            
            # Check if reading is within time threshold using milliseconds
            if response_reading['timestamp_ms'] >= time_threshold_ms:
                recent_readings.append(response_reading)
        
        # Sort by timestamp milliseconds descending (newest first)
        recent_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Calculate pagination
        total_items = len(recent_readings)
        total_pages = (total_items + limit - 1) // limit
        skip = (page - 1) * limit
        
        # Apply pagination
        paginated_readings = recent_readings[skip:skip + limit]
        
        # Remove timestamp_ms field
        for reading in paginated_readings:
            reading.pop('timestamp_ms', None)
        
        return {
            "data": paginated_readings,
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalItems": total_items,
                "itemsPerPage": limit,
                "hasNext": page < total_pages,
                "hasPrev": page > 1,
                "timeframe_hours": hours
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent temperature humidity data: {str(e)}")

@router.get("/stats", response_model=StatsResponse)
async def get_temperature_humidity_stats(
    hours: Optional[int] = Query(None, description="Time window in hours for statistics"),
    start_date: Optional[datetime] = Query(None, description="Start date for statistics"),
    end_date: Optional[datetime] = Query(None, description="End date for statistics")
):
    """
    Get statistics for temperature and humidity readings from esp32-2
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get the esp32-2 device
        device = await collection.find_one({"_id": "esp32-2"})
        
        if not device:
            return StatsResponse(
                temperature=ReadingStats(average=0, min=0, max=0),
                humidity=ReadingStats(average=0, min=0, max=0),
                total_readings=0
            )
        
        readings = device.get("readings", [])
        
        # Apply time filtering using milliseconds
        filtered_readings = []
        
        if hours:
            time_threshold_ms = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
            for i, reading in enumerate(readings):
                response_reading = temp_humidity_reading_helper(reading, "esp32-2", i)
                if response_reading['timestamp_ms'] >= time_threshold_ms:
                    filtered_readings.append(reading)
        elif start_date or end_date:
            start_ms = int(start_date.timestamp() * 1000) if start_date else 0
            end_ms = int(end_date.timestamp() * 1000) if end_date else float('inf')
            for i, reading in enumerate(readings):
                response_reading = temp_humidity_reading_helper(reading, "esp32-2", i)
                if start_ms <= response_reading['timestamp_ms'] <= end_ms:
                    filtered_readings.append(reading)
        else:
            filtered_readings = readings
        
        # Calculate statistics with proper data validation
        temperatures = []
        humidities = []
        
        for reading in filtered_readings:
            temp = reading.get("temperature")
            humidity = reading.get("humidity")
            
            # Validate and convert temperature
            if temp is not None:
                try:
                    temperatures.append(float(temp))
                except (ValueError, TypeError):
                    pass
            
            # Validate and convert humidity
            if humidity is not None:
                try:
                    humidities.append(float(humidity))
                except (ValueError, TypeError):
                    pass
        
        # Calculate statistics only if we have valid data
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
async def get_readings_count():
    """
    Get total count of temperature and humidity readings from esp32-2
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get the esp32-2 device
        device = await collection.find_one({"_id": "esp32-2"})
        
        if not device:
            return {"count": 0}
        
        # Get the readings array from the document
        readings_array = device.get("readings", [])
        
        count = len(readings_array)
        return {"count": count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting readings: {str(e)}")

@router.get("/test-document")
async def test_document():
    """
    Test endpoint to check if esp32-2 document exists and examine its structure
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get the esp32-2 document specifically
        document = await collection.find_one({"_id": "esp32-2"})
        
        if document:
            readings_count = len(document.get("readings", []))
            
            # Sample a few readings to examine structure
            sample_readings = []
            if readings_count > 0:
                sample_readings = document.get("readings", [])[:3]  # First 3 readings
            
            return {
                "exists": True,
                "readings_count": readings_count,
                "document_keys": list(document.keys()),
                "sample_readings": sample_readings
            }
        else:
            # Check what documents exist
            collections = await db.list_collection_names()
            all_documents = await collection.find().to_list(length=10)
            return {
                "exists": False,
                "collections": collections,
                "available_documents": [doc.get("_id", "unknown") for doc in all_documents]
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing document: {str(e)}")

@router.get("/readings/raw")
async def get_raw_readings_sample(limit: int = 5):
    """
    Return a raw sample (first `limit`) of readings from esp32-2 without any processing.
    Useful for debugging timestamp shapes and payload structure.
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        document = await collection.find_one({"_id": "esp32-2"})
        if not document:
            # return available document ids to help debug
            all_docs = await collection.find().to_list(length=20)
            return {"exists": False, "available_documents": [d.get("_id") for d in all_docs]}

        readings = document.get("readings", [])
        # return raw slice
        return {"count": len(readings), "sample": readings[:limit]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error returning raw readings sample: {str(e)}")

@router.get("/readings/range", response_model=List[TemperatureHumidityReadingResponse])
async def get_temperature_humidity_data_range(
    from_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    # Add aliases for the parameters
    from_: str = Query(None, alias="from"),
    to: str = Query(None, alias="to")
):
    """
    Get ALL temperature and humidity readings within a specific date range (no pagination)
    """
    try:
        # Use the first non-None value
        start_date = from_date or from_
        end_date = to_date or to

        if not start_date or not end_date:
            raise HTTPException(
                status_code=400,
                detail="Either from_date/from and to_date/to parameters are required"
            )

        db = await get_database()
        collection = db.sensor_readings
        
        # Convert string dates to datetime objects
        from_datetime = datetime.fromisoformat(start_date)
        to_datetime = datetime.fromisoformat(end_date)
        # Set end of day for to_date
        to_datetime = to_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Get the esp32-2 device
        device = await collection.find_one({"_id": "esp32-2"})
        
        if not device:
            return []
        
        readings = device.get("readings", [])
        filtered_readings = []
        
        # Convert timestamps and filter by date range
        for i, reading in enumerate(readings):
            response_reading = temp_humidity_reading_helper(reading, "esp32-2", i)
            reading_timestamp = response_reading['timestamp']
            
            if from_datetime <= reading_timestamp <= to_datetime:
                filtered_readings.append(response_reading)
        
        # Sort by timestamp (newest first)
        filtered_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Remove timestamp_ms field
        for reading in filtered_readings:
            reading.pop('timestamp_ms', None)
        
        return filtered_readings
        
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Please use YYYY-MM-DD format: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching date range data: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = await get_database()
        # Try to ping the database
        await db.command('ping')
        
        # Also check if esp32-2 exists
        collection = db.sensor_readings
        device = await collection.find_one({"_id": "esp32-2"})
        
        return {
            "status": "healthy", 
            "database": "connected",
            "esp32-2_exists": device is not None,
            "esp32-2_readings": len(device.get("readings", [])) if device else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Make sure the router is exported
__all__ = ["router"]