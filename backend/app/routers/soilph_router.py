# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from datetime import datetime
# from typing import List, Optional
# import os
# from app.services.database import get_database

# router = APIRouter(prefix="/api/soil-ph", tags=["Soil pH"])

# # Pydantic models for request/response
# class SoilPhResponse(BaseModel):
#     id: str
#     timestamp: float
#     date: str
#     time: str
#     deviceId: str
#     soilPh: str
#     phStatus: str
#     nitrogen: Optional[str] = None
#     phosphorus: Optional[str] = None
#     potassium: Optional[str] = None

# # Helper functions
# def format_date(date):
#     if not date:
#         return '--'
#     months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     day = date.day
#     month = months[date.month - 1]
#     year = date.year
#     return f"{month} {day:02d}, {year}"

# def format_time(date):
#     if not date:
#         return '--'
#     hours = date.hour
#     minutes = date.minute
#     seconds = date.second
#     ampm = 'AM' if hours < 12 else 'PM'
#     hours = hours % 12
#     hours = 12 if hours == 0 else hours
#     return f"{hours:02d}:{minutes:02d}:{seconds:02d} {ampm}"

# def convert_firebase_timestamp(timestamp_dict):
#     """Convert Firebase timestamp object to datetime"""
#     if isinstance(timestamp_dict, dict) and '_seconds' in timestamp_dict:
#         return datetime.fromtimestamp(timestamp_dict['_seconds'] + timestamp_dict.get('_nanoseconds', 0) / 1e9)
#     return datetime.now()

# def calculate_ph_status(ph_value):
#     """Calculate pH status based on pH value"""
#     if ph_value is None:
#         return "UNKNOWN"
#     ph_num = float(ph_value)
#     if ph_num < 6.6:
#         return "ACIDIC"
#     elif 6.6 <= ph_num <= 7.3:
#         return "NEUTRAL"
#     else:
#         return "ALKALINE"

# # API endpoints
# @router.get("/readings", response_model=List[SoilPhResponse])
# async def get_soil_ph_readings():
#     try:
#         db = await get_database()
#         # Get the esp32-1 document which contains the readings array
#         doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
#         if not doc or "readings" not in doc:
#             return []
        
#         # Process the readings array - filter for soil pH readings
#         results = []
#         for reading in doc["readings"]:
#             if "soilPh" in reading and reading["soilPh"] is not None:
#                 timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                
#                 results.append({
#                     "id": reading.get("_id", ""),
#                     "timestamp": timestamp.timestamp(),
#                     "date": format_date(timestamp),
#                     "time": format_time(timestamp),
#                     "deviceId": reading.get("device_id", "esp32-1"),
#                     "soilPh": f"{reading.get('soilPh', 0):.1f}",
#                     "phStatus": calculate_ph_status(reading.get('soilPh')),
#                     "nitrogen": f"{reading.get('nitrogen', 0):.0f}" if reading.get('nitrogen') is not None else "--",
#                     "phosphorus": f"{reading.get('phosphorus', 0):.0f}" if reading.get('phosphorus') is not None else "--",
#                     "potassium": f"{reading.get('potassium', 0):.0f}" if reading.get('potassium') is not None else "--"
#                 })
        
#         # Sort by timestamp descending
#         results.sort(key=lambda x: x["timestamp"], reverse=True)
        
#         return results
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching soil pH data: {str(e)}")

# @router.get("/readings/realtime", response_model=List[SoilPhResponse])
# async def get_realtime_soil_ph():
#     try:
#         db = await get_database()
#         # Get the esp32-1 document
#         doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
#         if not doc or "readings" not in doc:
#             return []
        
#         # Get readings from the last 5 minutes
#         five_minutes_ago = datetime.now().timestamp() - 300
        
#         # Process recent readings
#         results = []
#         for reading in doc["readings"]:
#             if "soilPh" in reading and reading["soilPh"] is not None:
#                 timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                
#                 if timestamp.timestamp() >= five_minutes_ago:
#                     results.append({
#                         "id": reading.get("_id", ""),
#                         "timestamp": timestamp.timestamp(),
#                         "date": format_date(timestamp),
#                         "time": format_time(timestamp),
#                         "deviceId": reading.get("device_id", "esp32-1"),
#                         "soilPh": f"{reading.get('soilPh', 0):.1f}",
#                         "phStatus": calculate_ph_status(reading.get('soilPh')),
#                         "nitrogen": f"{reading.get('nitrogen', 0):.0f}" if reading.get('nitrogen') is not None else "--",
#                         "phosphorus": f"{reading.get('phosphorus', 0):.0f}" if reading.get('phosphorus') is not None else "--",
#                         "potassium": f"{reading.get('potassium', 0):.0f}" if reading.get('potassium') is not None else "--"
#                     })
        
#         # Sort by timestamp descending and limit to 20 most recent
#         results.sort(key=lambda x: x["timestamp"], reverse=True)
#         return results[:20]
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching real-time soil pH data: {str(e)}")

# @router.get("/stats")
# async def get_soil_ph_stats(hours: int = 24):
#     try:
#         db = await get_database()
#         # Get the esp32-1 document
#         doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
#         if not doc or "readings" not in doc:
#             return {"min": 0, "max": 0, "avg": 0, "count": 0}
        
#         # Calculate time threshold
#         time_threshold = datetime.now().timestamp() - (hours * 3600)
        
#         # Extract soil pH values from recent readings
#         soil_ph_values = []
#         for reading in doc["readings"]:
#             if "soilPh" in reading and reading["soilPh"] is not None:
#                 timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
#                 if timestamp.timestamp() >= time_threshold:
#                     soil_ph_values.append(float(reading["soilPh"]))
        
#         if not soil_ph_values:
#             return {"min": 0, "max": 0, "avg": 0, "count": 0}
        
#         # Calculate statistics
#         return {
#             "min": min(soil_ph_values),
#             "max": max(soil_ph_values),
#             "avg": sum(soil_ph_values) / len(soil_ph_values),
#             "count": len(soil_ph_values)
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error calculating soil pH statistics: {str(e)}")

# @router.get("/search")
# async def search_soil_ph(query: str, limit: int = 50):
#     try:
#         db = await get_database()
#         # Get the esp32-1 document
#         doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
#         if not doc or "readings" not in doc:
#             return []
        
#         # Search through readings
#         results = []
#         for reading in doc["readings"]:
#             if "soilPh" in reading and reading["soilPh"] is not None:
#                 # Check if query matches any field
#                 matches = any(
#                     str(value).lower().find(query.lower()) != -1 
#                     for key, value in reading.items() 
#                     if key not in ['_id', 'timestamp', 'device_id'] and value is not None
#                 )
                
#                 if matches:
#                     timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                    
#                     results.append({
#                         "id": reading.get("_id", ""),
#                         "timestamp": timestamp.timestamp(),
#                         "date": format_date(timestamp),
#                         "time": format_time(timestamp),
#                         "deviceId": reading.get("device_id", "esp32-1"),
#                         "soilPh": f"{reading.get('soilPh', 0):.1f}",
#                         "phStatus": calculate_ph_status(reading.get('soilPh')),
#                         "nitrogen": f"{reading.get('nitrogen', 0):.0f}" if reading.get('nitrogen') is not None else "--",
#                         "phosphorus": f"{reading.get('phosphorus', 0):.0f}" if reading.get('phosphorus') is not None else "--",
#                         "potassium": f"{reading.get('potassium', 0):.0f}" if reading.get('potassium') is not None else "--"
#                     })
        
#         # Sort by timestamp descending and limit results
#         results.sort(key=lambda x: x["timestamp"], reverse=True)
#         return results[:limit]
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error searching soil pH data: {str(e)}")

# @router.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     try:
#         db = await get_database()
#         # Try to access the collection
#         doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
#         return {
#             "status": "healthy",
#             "message": "Soil pH API is working",
#             "has_data": doc is not None and "readings" in doc
#         }
#     except Exception as e:
#         return {
#             "status": "unhealthy",
#             "error": str(e),
#             "message": "Soil pH API connection failed"
#         }

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from app.services.database import get_database
from bson import ObjectId
import motor.motor_asyncio

router = APIRouter(prefix="/api/soil-ph", tags=["Soil pH"])

# Pydantic models
class SoilPhReadingResponse(BaseModel):
    id: str
    device_id: str
    soilPh: float
    timestamp: datetime
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    moisture: Optional[float] = None

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class PaginatedSoilPhResponse(BaseModel):
    data: List[SoilPhReadingResponse]
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
def soilph_reading_helper(reading, device_id, index=None) -> dict:
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
    
    # Calculate pH status
    soil_ph_value = reading.get("soilPh")
    if soil_ph_value is not None:
        if soil_ph_value < 6.6:
            ph_status = "ACIDIC"
        elif 6.6 <= soil_ph_value <= 7.3:
            ph_status = "NEUTRAL"
        else:
            ph_status = "ALKALINE"
    else:
        ph_status = "UNKNOWN"
    
    return {
        "id": reading_id,
        "device_id": device_id,
        "soilPh": reading.get("soilPh"),
        "phStatus": ph_status,
        "timestamp": timestamp,
        "timestamp_ms": timestamp_ms,  # For accurate sorting
        "nitrogen": reading.get("nitrogen"),
        "phosphorus": reading.get("phosphorus"),
        "potassium": reading.get("potassium"),
        "temperature": reading.get("temperature"),
        "humidity": reading.get("humidity"),
        "moisture": reading.get("moisture")
    }

@router.get("/readings", response_model=PaginatedSoilPhResponse)
async def get_soil_ph_readings(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Get paginated Soil pH sensor readings from esp32-1 device, sorted by timestamp (newest first)
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
        
        # Process each reading from esp32-1 that has soil pH data
        for i, reading in enumerate(readings):
            # Only include readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                # Create response object
                response_reading = soilph_reading_helper(reading, "esp32-1", i)
                all_readings.append(response_reading)
        
        # Sort by timestamp milliseconds descending (newest first)
        all_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Calculate pagination
        total_items = len(all_readings)
        total_pages = (total_items + limit - 1) // limit  # Ceiling division
        skip = (page - 1) * limit
        
        # Apply pagination
        paginated_readings = all_readings[skip:skip + limit]
        
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
        raise HTTPException(status_code=500, detail=f"Error fetching soil pH data: {str(e)}")

@router.get("/readings/all", response_model=List[SoilPhReadingResponse])
async def get_all_soil_ph_readings():
    """
    Get ALL soil pH sensor readings (use with caution for large datasets)
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
        readings = device.get("readings", [])
        all_readings = []
        
        for i, reading in enumerate(readings):
            # Only include readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                response_reading = soilph_reading_helper(reading, "esp32-1", i)
                all_readings.append(response_reading)
        
        # Sort by timestamp milliseconds descending (newest first)
        all_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Remove timestamp_ms field
        for reading in all_readings:
            reading.pop('timestamp_ms', None)
        
        return all_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all soil pH data: {str(e)}")

@router.get("/readings/realtime", response_model=List[SoilPhReadingResponse])
async def get_realtime_soil_ph():
    """
    Get real-time soil pH sensor readings from esp32-1 (last 5 minutes)
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Calculate time threshold in milliseconds (last 5 minutes)
        time_threshold_ms = int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)
        
        # Get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
        readings = device.get("readings", [])
        recent_readings = []
        
        for i, reading in enumerate(readings):
            # Only include readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                response_reading = soilph_reading_helper(reading, "esp32-1", i)
                
                # Check if reading is within time threshold using milliseconds
                if response_reading['timestamp_ms'] >= time_threshold_ms:
                    recent_readings.append(response_reading)
        
        # Sort by timestamp milliseconds descending (newest first)
        recent_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Limit to 20 most recent readings
        recent_readings = recent_readings[:20]
        
        # Remove timestamp_ms field
        for reading in recent_readings:
            reading.pop('timestamp_ms', None)
        
        return recent_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching real-time soil pH data: {str(e)}")

@router.get("/readings/recent", response_model=PaginatedSoilPhResponse)
async def get_recent_soil_ph_readings(
    hours: int = Query(1, ge=1, le=24),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get recent soil pH sensor readings from esp32-1 with pagination
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
        
        for i, reading in enumerate(readings):
            # Only include readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                response_reading = soilph_reading_helper(reading, "esp32-1", i)
                
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
        raise HTTPException(status_code=500, detail=f"Error fetching recent soil pH data: {str(e)}")

@router.get("/stats")
async def get_soil_ph_stats(
    hours: int = Query(24, ge=1, le=168, description="Timeframe in hours (1-168)")
):
    """
    Get soil pH statistics for the specified timeframe
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
        soil_ph_values = []
        total_readings = 0
        
        for i, reading in enumerate(readings):
            # Only process readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                response_reading = soilph_reading_helper(reading, "esp32-1", i)
                
                # Check if reading is within time threshold using milliseconds
                if response_reading['timestamp_ms'] >= time_threshold_ms:
                    soil_ph = reading.get('soilPh')
                    
                    # Only include valid numeric values
                    if soil_ph is not None and not isinstance(soil_ph, str):
                        soil_ph_values.append(float(soil_ph))
                    
                    total_readings += 1
        
        if soil_ph_values:
            return {
                "timeframe_hours": hours,
                "total_readings": total_readings,
                "min": round(min(soil_ph_values), 1),
                "max": round(max(soil_ph_values), 1),
                "avg": round(sum(soil_ph_values) / len(soil_ph_values), 1),
                "count": len(soil_ph_values)
            }
        else:
            return {
                "timeframe_hours": hours,
                "total_readings": 0,
                "min": 0,
                "max": 0,
                "avg": 0,
                "count": 0
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating soil pH statistics: {str(e)}")

@router.get("/readings/range", response_model=PaginatedSoilPhResponse)
async def get_soil_ph_readings_range(
    from_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    # Add aliases for the parameters
    from_: str = Query(None, alias="from"),
    to: str = Query(None, alias="to")
):
    """
    Get soil pH sensor readings within a specific date range
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
        
        # Get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
        readings = device.get("readings", [])
        filtered_readings = []
        
        # Convert timestamps and filter by date range
        for i, reading in enumerate(readings):
            # Only include readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                response_reading = soilph_reading_helper(reading, "esp32-1", i)
                reading_timestamp = response_reading['timestamp']
                
                if from_datetime <= reading_timestamp <= to_datetime:
                    filtered_readings.append(response_reading)
        
        # Sort by timestamp (newest first)
        filtered_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Remove timestamp_ms field
        for reading in filtered_readings:
            reading.pop('timestamp_ms', None)
        
        return {
            "data": filtered_readings,
            "pagination": {
                "totalItems": len(filtered_readings),
                "returnedItems": len(filtered_readings),
                "hasMore": False,
                "dateRange": {
                    "from": from_datetime.isoformat(),
                    "to": to_datetime.isoformat()
                }
            }
        }
        
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

@router.get("/readings/search")
async def search_soil_ph_readings(
    query: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Search soil pH readings by various criteria
    """
    try:
        db = await get_database()
        collection = db.sensor_readings
        
        # Get the esp32-1 device
        device = await collection.find_one({"_id": "esp32-1"})
        
        if not device:
            raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
        readings = device.get("readings", [])
        search_results = []
        
        for i, reading in enumerate(readings):
            # Only include readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                # Check if query matches any field
                matches = False
                for key, value in reading.items():
                    if key not in ['_id', 'timestamp', 'device_id'] and value is not None:
                        if query.lower() in str(value).lower():
                            matches = True
                            break
                
                if matches:
                    response_reading = soilph_reading_helper(reading, "esp32-1", i)
                    search_results.append(response_reading)
        
        # Sort by timestamp (newest first)
        search_results.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Calculate pagination
        total_items = len(search_results)
        total_pages = (total_items + limit - 1) // limit
        skip = (page - 1) * limit
        
        # Apply pagination
        paginated_results = search_results[skip:skip + limit]
        
        # Remove timestamp_ms field
        for reading in paginated_results:
            reading.pop('timestamp_ms', None)
        
        return {
            "data": paginated_results,
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalItems": total_items,
                "itemsPerPage": limit,
                "hasNext": page < total_pages,
                "hasPrev": page > 1,
                "searchQuery": query
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching soil pH data: {str(e)}")

@router.get("/debug-sorted")
async def debug_sorted_soil_ph_data():
    """
    Debug endpoint to verify sorting order with timestamps for soil pH data
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
        
        # Process readings with timestamps that have soil pH data
        for i, reading in enumerate(readings):
            # Only include readings that have soil pH data
            if "soilPh" in reading and reading["soilPh"] is not None:
                response_reading = soilph_reading_helper(reading, "esp32-1", i)
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
                "soilPh": reading['soilPh'],
                "phStatus": reading['phStatus']
            })
        
        # Oldest 5 readings
        for i, reading in enumerate(sorted_readings[-5:]):
            debug_info["oldest_5_readings"].append({
                "position": len(sorted_readings) - 4 + i,
                "id": reading['id'],
                "timestamp": reading['timestamp'].isoformat(),
                "timestamp_ms": reading['timestamp_ms'],
                "soilPh": reading['soilPh'],
                "phStatus": reading['phStatus']
            })
        
        return debug_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for soil pH API"""
    try:
        db = await get_database()
        # Try to ping the database
        await db.command('ping')
        
        # Also check if esp32-1 exists and has soil pH data
        collection = db.sensor_readings
        device = await collection.find_one({"_id": "esp32-1"})
        
        soil_ph_readings_count = 0
        if device:
            readings = device.get("readings", [])
            # Count only readings that have soil pH data
            soil_ph_readings_count = sum(1 for reading in readings if "soilPh" in reading and reading["soilPh"] is not None)
        
        return {
            "status": "healthy", 
            "database": "connected",
            "esp32-1_exists": device is not None,
            "total_readings": len(device.get("readings", [])) if device else 0,
            "soil_ph_readings": soil_ph_readings_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")