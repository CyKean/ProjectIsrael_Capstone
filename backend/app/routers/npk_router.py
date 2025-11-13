# from fastapi import APIRouter, HTTPException, Query
# from datetime import datetime, timedelta
# from typing import List, Optional
# from pydantic import BaseModel
# from app.services.database import get_database
# from bson import ObjectId
# import motor.motor_asyncio

# router = APIRouter(prefix="/api", tags=["NPK Data"])

# # Pydantic models
# class NPKReadingResponse(BaseModel):
#     id: str
#     device_id: str
#     nitrogen: float
#     phosphorus: float
#     potassium: float
#     timestamp: datetime
#     soilPh: Optional[float] = None
#     temperature: Optional[float] = None
#     humidity: Optional[float] = None
#     moisture: Optional[float] = None

#     class Config:
#         json_encoders = {
#             ObjectId: str,
#             datetime: lambda v: v.isoformat()
#         }

# # Helper function to convert timestamp to milliseconds for accurate sorting
# def get_timestamp_ms(timestamp_obj):
#     """Convert various timestamp formats to milliseconds since epoch"""
#     if isinstance(timestamp_obj, dict) and '_seconds' in timestamp_obj:
#         # Firebase timestamp format: {_seconds: 123456789, _nanoseconds: 123000000}
#         return timestamp_obj['_seconds'] * 1000 + timestamp_obj.get('_nanoseconds', 0) // 1000000
#     elif isinstance(timestamp_obj, datetime):
#         # Python datetime object
#         return int(timestamp_obj.timestamp() * 1000)
#     elif isinstance(timestamp_obj, (int, float)):
#         # Already in milliseconds or seconds
#         if timestamp_obj > 1e12:  # Likely milliseconds
#             return int(timestamp_obj)
#         else:  # Likely seconds
#             return int(timestamp_obj * 1000)
#     else:
#         # Default to current time
#         return int(datetime.now().timestamp() * 1000)

# # Helper function to convert MongoDB reading to response model
# def npk_reading_helper(reading, device_id) -> dict:
#     # Convert timestamp to datetime and get milliseconds for sorting
#     timestamp_obj = reading.get('timestamp')
    
#     # Get timestamp in milliseconds for accurate sorting
#     timestamp_ms = get_timestamp_ms(timestamp_obj)
    
#     # Convert to datetime object for response
#     if isinstance(timestamp_obj, dict) and '_seconds' in timestamp_obj:
#         timestamp = datetime.fromtimestamp(timestamp_obj['_seconds'])
#     elif isinstance(timestamp_obj, datetime):
#         timestamp = timestamp_obj
#     elif isinstance(timestamp_obj, (int, float)):
#         # Convert from milliseconds or seconds to datetime
#         if timestamp_obj > 1e12:  # Milliseconds
#             timestamp = datetime.fromtimestamp(timestamp_obj / 1000)
#         else:  # Seconds
#             timestamp = datetime.fromtimestamp(timestamp_obj)
#     else:
#         timestamp = datetime.now()
    
#     return {
#         "id": str(reading.get("_id", ObjectId())),
#         "device_id": device_id,
#         "nitrogen": reading.get("nitrogen", 0),
#         "phosphorus": reading.get("phosphorus", 0),
#         "potassium": reading.get("potassium", 0),
#         "soilPh": reading.get("soilPh"),
#         "timestamp": timestamp,
#         "timestamp_ms": timestamp_ms,  # For accurate sorting
#         "temperature": reading.get("temperature"),
#         "humidity": reading.get("humidity"),
#         "moisture": reading.get("moisture")
#     }

# @router.get("/npk-data", response_model=List[NPKReadingResponse])
# async def get_npk_data():
#     """
#     Get all NPK sensor readings from esp32-1 device, sorted by timestamp (newest first)
#     """
#     try:
#         db = await get_database()
#         collection = db.sensor_readings
        
#         # Specifically get the esp32-1 device
#         device = await collection.find_one({"_id": "esp32-1"})
        
#         if not device:
#             raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
#         readings = device.get("readings", [])
#         all_readings = []
        
#         # Process each reading from esp32-1
#         for reading in readings:
#             # Create response object
#             response_reading = npk_reading_helper(reading, "esp32-1")
#             all_readings.append(response_reading)
        
#         # Sort by timestamp milliseconds descending (newest first) - MOST ACCURATE
#         all_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
#         # Remove the temporary timestamp_ms field before returning
#         for reading in all_readings:
#             reading.pop('timestamp_ms', None)
        
#         return all_readings
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching NPK data: {str(e)}")

# @router.get("/npk-data/recent", response_model=List[NPKReadingResponse])
# async def get_recent_npk_data(
#     hours: int = Query(1, ge=1, le=24),
#     limit: int = Query(20, ge=1, le=100)
# ):
#     """
#     Get recent NPK sensor readings from esp32-1
#     """
#     try:
#         db = await get_database()
#         collection = db.sensor_readings
        
#         # Calculate time threshold in milliseconds
#         time_threshold_ms = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        
#         # Get the esp32-1 device
#         device = await collection.find_one({"_id": "esp32-1"})
        
#         if not device:
#             raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
#         readings = device.get("readings", [])
#         recent_readings = []
        
#         for reading in readings:
#             response_reading = npk_reading_helper(reading, "esp32-1")
            
#             # Check if reading is within time threshold using milliseconds
#             if response_reading['timestamp_ms'] >= time_threshold_ms:
#                 recent_readings.append(response_reading)
        
#         # Sort by timestamp milliseconds descending (newest first)
#         recent_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
#         recent_readings = recent_readings[:limit]
        
#         # Remove the temporary timestamp_ms field
#         for reading in recent_readings:
#             reading.pop('timestamp_ms', None)
        
#         return recent_readings
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching recent NPK data: {str(e)}")

# @router.get("/npk-data/stats/summary")
# async def get_npk_stats_summary(
#     days: int = Query(7, ge=1, le=365)
# ):
#     """
#     Get summary statistics for NPK readings from esp32-1
#     """
#     try:
#         db = await get_database()
#         collection = db.sensor_readings
        
#         # Calculate time threshold in milliseconds
#         time_threshold_ms = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
#         # Get the esp32-1 device
#         device = await collection.find_one({"_id": "esp32-1"})
        
#         if not device:
#             raise HTTPException(status_code=404, detail="Device esp32-1 not found")
        
#         readings = device.get("readings", [])
#         all_nitrogen = []
#         all_phosphorus = []
#         all_potassium = []
#         total_readings = 0
        
#         for reading in readings:
#             response_reading = npk_reading_helper(reading, "esp32-1")
            
#             # Check if reading is within time threshold using milliseconds
#             if response_reading['timestamp_ms'] >= time_threshold_ms:
#                 nitrogen = reading.get('nitrogen')
#                 phosphorus = reading.get('phosphorus')
#                 potassium = reading.get('potassium')
                
#                 # Only include valid numeric values
#                 if nitrogen is not None and not isinstance(nitrogen, str):
#                     all_nitrogen.append(float(nitrogen))
#                 if phosphorus is not None and not isinstance(phosphorus, str):
#                     all_phosphorus.append(float(phosphorus))
#                 if potassium is not None and not isinstance(potassium, str):
#                     all_potassium.append(float(potassium))
                
#                 total_readings += 1
        
#         if total_readings > 0:
#             return {
#                 "total_readings": total_readings,
#                 "nitrogen": {
#                     "average": round(sum(all_nitrogen) / len(all_nitrogen), 2) if all_nitrogen else 0,
#                     "min": round(min(all_nitrogen), 2) if all_nitrogen else 0,
#                     "max": round(max(all_nitrogen), 2) if all_nitrogen else 0
#                 },
#                 "phosphorus": {
#                     "average": round(sum(all_phosphorus) / len(all_phosphorus), 2) if all_phosphorus else 0,
#                     "min": round(min(all_phosphorus), 2) if all_phosphorus else 0,
#                     "max": round(max(all_phosphorus), 2) if all_phosphorus else 0
#                 },
#                 "potassium": {
#                     "average": round(sum(all_potassium) / len(all_potassium), 2) if all_potassium else 0,
#                     "min": round(min(all_potassium), 2) if all_potassium else 0,
#                     "max": round(max(all_potassium), 2) if all_potassium else 0
#                 }
#             }
#         else:
#             return {
#                 "total_readings": 0,
#                 "nitrogen": {"average": 0, "min": 0, "max": 0},
#                 "phosphorus": {"average": 0, "min": 0, "max": 0},
#                 "potassium": {"average": 0, "min": 0, "max": 0}
#             }
            
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

# @router.get("/npk-data/debug-sorted")
# async def debug_sorted_data():
#     """
#     Debug endpoint to verify sorting order with timestamps
#     """
#     try:
#         db = await get_database()
#         collection = db.sensor_readings
        
#         # Get the esp32-1 device
#         device = await collection.find_one({"_id": "esp32-1"})
        
#         if not device:
#             return {"error": "Device esp32-1 not found"}
        
#         readings = device.get("readings", [])
#         sorted_readings = []
        
#         # Process readings with timestamps
#         for reading in readings:
#             response_reading = npk_reading_helper(reading, "esp32-1")
#             sorted_readings.append(response_reading)
        
#         # Sort by timestamp milliseconds (newest first)
#         sorted_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
#         # Prepare debug info
#         debug_info = {
#             "total_readings": len(sorted_readings),
#             "sorting_method": "timestamp_ms descending (newest first)",
#             "newest_5_readings": [],
#             "oldest_5_readings": []
#         }
        
#         # Newest 5 readings
#         for i, reading in enumerate(sorted_readings[:5]):
#             debug_info["newest_5_readings"].append({
#                 "position": i + 1,
#                 "id": reading['id'],
#                 "timestamp": reading['timestamp'].isoformat(),
#                 "timestamp_ms": reading['timestamp_ms'],
#                 "nitrogen": reading['nitrogen'],
#                 "phosphorus": reading['phosphorus'],
#                 "potassium": reading['potassium']
#             })
        
#         # Oldest 5 readings
#         for i, reading in enumerate(sorted_readings[-5:]):
#             debug_info["oldest_5_readings"].append({
#                 "position": len(sorted_readings) - 4 + i,
#                 "id": reading['id'],
#                 "timestamp": reading['timestamp'].isoformat(),
#                 "timestamp_ms": reading['timestamp_ms'],
#                 "nitrogen": reading['nitrogen'],
#                 "phosphorus": reading['phosphorus'],
#                 "potassium": reading['potassium']
#             })
        
#         return debug_info
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")

# @router.get("/npk-data/debug")
# async def debug_npk_data():
#     """
#     Debug endpoint to see database structure
#     """
#     try:
#         db = await get_database()
#         collection = db.sensor_readings
        
#         # Get the esp32-1 device
#         device = await collection.find_one({"_id": "esp32-1"})
        
#         if not device:
#             return {"error": "Device esp32-1 not found"}
        
#         debug_info = {
#             "device_id": device["_id"],
#             "total_readings": len(device.get("readings", [])),
#             "sample_readings": []
#         }
        
#         # Sample readings with timestamp info
#         for i, reading in enumerate(device.get("readings", [])[:3]):
#             timestamp_ms = get_timestamp_ms(reading.get('timestamp'))
#             debug_info["sample_readings"].append({
#                 "index": i,
#                 "has_id": "_id" in reading,
#                 "id_value": str(reading.get("_id", "MISSING")),
#                 "nitrogen": reading.get("nitrogen"),
#                 "phosphorus": reading.get("phosphorus"),
#                 "potassium": reading.get("potassium"),
#                 "timestamp_raw": reading.get("timestamp"),
#                 "timestamp_type": type(reading.get("timestamp")).__name__ if reading.get("timestamp") else "None",
#                 "timestamp_ms": timestamp_ms
#             })
        
#         return debug_info
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")

from fastapi import Query, APIRouter, HTTPException, Query
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

class PaginatedNPKResponse(BaseModel):
    data: List[NPKReadingResponse]
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
def npk_reading_helper(reading, device_id, index=None) -> dict:
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

@router.get("/npk-data", response_model=PaginatedNPKResponse)
async def get_npk_data(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Get paginated NPK sensor readings from esp32-1 device, sorted by timestamp (newest first)
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
        for i, reading in enumerate(readings):
            # Create response object
            response_reading = npk_reading_helper(reading, "esp32-1", i)
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
        raise HTTPException(status_code=500, detail=f"Error fetching NPK data: {str(e)}")

@router.get("/npk-data/all", response_model=List[NPKReadingResponse])
async def get_all_npk_data():
    """
    Get ALL NPK sensor readings (use with caution for large datasets)
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
            response_reading = npk_reading_helper(reading, "esp32-1", i)
            all_readings.append(response_reading)
        
        # Sort by timestamp milliseconds descending (newest first)
        all_readings.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        
        # Remove timestamp_ms field
        for reading in all_readings:
            reading.pop('timestamp_ms', None)
        
        return all_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all NPK data: {str(e)}")

@router.get("/npk-data/recent", response_model=PaginatedNPKResponse)
async def get_recent_npk_data(
    hours: int = Query(1, ge=1, le=24),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get recent NPK sensor readings from esp32-1 with pagination
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
            response_reading = npk_reading_helper(reading, "esp32-1", i)
            
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
        raise HTTPException(status_code=500, detail=f"Error fetching recent NPK data: {str(e)}")

# Keep your existing endpoints but update the helper function calls
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
        
        for i, reading in enumerate(readings):
            response_reading = npk_reading_helper(reading, "esp32-1", i)
            
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

# Update your existing debug endpoints to use the new helper function
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
        for i, reading in enumerate(readings):
            response_reading = npk_reading_helper(reading, "esp32-1", i)
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
    
@router.get("/npk-data/range", response_model=PaginatedNPKResponse)
async def get_npk_data_range(
    from_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    # Add aliases for the parameters
    from_: str = Query(None, alias="from"),
    to: str = Query(None, alias="to")
):
    """
    Get NPK sensor readings within a specific date range
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
            response_reading = npk_reading_helper(reading, "esp32-1", i)
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


