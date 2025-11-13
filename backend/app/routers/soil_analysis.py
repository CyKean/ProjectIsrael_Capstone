# from fastapi import APIRouter, HTTPException
# from pymongo import DESCENDING
# from pydantic import BaseModel
# from datetime import datetime
# from typing import List, Optional
# import os
# from app.services.database import get_database

# router = APIRouter(prefix="/api/soil-analysis", tags=["Soil Analysis"])

# # Pydantic models for request/response
# class ESP32Response(BaseModel):
#     id: str
#     timestamp: float
#     date: str
#     time: str
#     deviceId: str
#     nitrogen: Optional[str] = None
#     phosphorus: Optional[str] = None
#     potassium: Optional[str] = None
#     ph: Optional[str] = None
#     temperature: Optional[str] = None
#     humidity: Optional[str] = None
#     soilMoisture: Optional[str] = None

# # Helper functions
# def format_date(date):
#     if not date:
#         return '--'
#     months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     day = date.day
#     month = months[date.month - 1]
#     year = date.year
#     return f"{month} {day}, {year}"

# def format_time(date):
#     if not date:
#         return '--'
#     hours = date.hour
#     minutes = date.minute
#     ampm = 'AM' if hours < 12 else 'PM'
#     hours = hours % 12
#     hours = 12 if hours == 0 else hours
#     return f"{hours:02d}:{minutes:02d} {ampm}"

# def convert_firebase_timestamp(timestamp_dict):
#     """Convert Firebase timestamp object to datetime"""
#     if isinstance(timestamp_dict, dict) and '_seconds' in timestamp_dict:
#         return datetime.fromtimestamp(timestamp_dict['_seconds'] + timestamp_dict.get('_nanoseconds', 0) / 1e9)
#     return datetime.now()

# # API endpoints - fixed to match your database structure
# @router.get("/esp32-1", response_model=List[ESP32Response])
# async def get_esp32_1_data():
#     try:
#         db = await get_database()
#         # Get the esp32-1 document which contains the readings array
#         doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
#         if not doc or "readings" not in doc:
#             return []
        
#         # Process the readings array
#         results = []
#         for reading in doc["readings"]:
#             timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
            
#             results.append({
#                 "id": reading.get("_id", ""),
#                 "timestamp": timestamp.timestamp(),
#                 "date": format_date(timestamp),
#                 "time": format_time(timestamp),
#                 "deviceId": reading.get("device_id", "esp32-1"),
#                 "nitrogen": f"{reading.get('nitrogen', 0):.2f}" if reading.get('nitrogen') is not None else "--",
#                 "phosphorus": f"{reading.get('phosphorus', 0):.2f}" if reading.get('phosphorus') is not None else "--",
#                 "potassium": f"{reading.get('potassium', 0):.2f}" if reading.get('potassium') is not None else "--",
#                 "ph": f"{reading.get('soilPh', 0):.2f}" if reading.get('soilPh') is not None else "--"
#             })
        
#         # Sort by timestamp descending
#         results.sort(key=lambda x: x["timestamp"], reverse=True)
#         return results
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching ESP32-1 data: {str(e)}")

# @router.get("/esp32-2", response_model=List[ESP32Response])
# async def get_esp32_2_data():
#     try:
#         db = await get_database()
#         # Get the esp32-2 document which contains the readings array
#         doc = await db.sensor_readings.find_one({"_id": "esp32-2"})
        
#         if not doc or "readings" not in doc:
#             return []
        
#         # Process the readings array
#         results = []
#         for reading in doc["readings"]:
#             timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
            
#             results.append({
#                 "id": reading.get("_id", ""),
#                 "timestamp": timestamp.timestamp(),
#                 "date": format_date(timestamp),
#                 "time": format_time(timestamp),
#                 "deviceId": reading.get("device_id", "esp32-2"),
#                 "temperature": f"{reading.get('temperature', 0):.2f}" if reading.get('temperature') is not None else "--",
#                 "humidity": f"{reading.get('humidity', 0):.2f}" if reading.get('humidity') is not None else "--",
#                 "soilMoisture": f"{reading.get('soilMoisture', 0):.2f}" if reading.get('soilMoisture') is not None else "--"
#             })
        
#         # Sort by timestamp descending
#         results.sort(key=lambda x: x["timestamp"], reverse=True)
#         return results
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching ESP32-2 data: {str(e)}")

# # Update global search to match new structure
# @router.get("/global-search")
# async def global_search(query: str):
#     try:
#         db = await get_database()
#         results = []
        
#         # Search both esp32-1 and esp32-2 documents
#         for device_id in ["esp32-1", "esp32-2"]:
#             doc = await db.sensor_readings.find_one({"_id": device_id})
            
#             if not doc or "readings" not in doc:
#                 continue
            
#             for reading in doc["readings"]:
#                 # Check if any field contains the query
#                 matches = any(
#                     str(value).lower().find(query.lower()) != -1 
#                     for key, value in reading.items() 
#                     if key not in ['_id', 'timestamp', 'device_id'] and value is not None
#                 )
                
#                 if matches:
#                     timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
                    
#                     device_data = {
#                         "id": reading.get("_id", ""),
#                         "timestamp": timestamp.timestamp(),
#                         "date": format_date(timestamp),
#                         "time": format_time(timestamp),
#                         "deviceId": device_id
#                     }
                    
#                     if device_id == "esp32-1":
#                         device_data.update({
#                             "nitrogen": f"{reading.get('nitrogen', 0):.2f}" if reading.get('nitrogen') is not None else "--",
#                             "phosphorus": f"{reading.get('phosphorus', 0):.2f}" if reading.get('phosphorus') is not None else "--",
#                             "potassium": f"{reading.get('potassium', 0):.2f}" if reading.get('potassium') is not None else "--",
#                             "ph": f"{reading.get('soilPh', 0):.2f}" if reading.get('soilPh') is not None else "--"
#                         })
#                     else:
#                         device_data.update({
#                             "temperature": f"{reading.get('temperature', 0):.2f}" if reading.get('temperature') is not None else "--",
#                             "humidity": f"{reading.get('humidity', 0):.2f}" if reading.get('humidity') is not None else "--",
#                             "soilMoisture": f"{reading.get('soilMoisture', 0):.2f}" if reading.get('soilMoisture') is not None else "--"
#                         })
                    
#                     results.append(device_data)
        
#         # Sort by timestamp descending
#         results.sort(key=lambda x: x["timestamp"], reverse=True)
#         return results
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error performing global search: {str(e)}")

from fastapi import APIRouter, HTTPException, Query
from pymongo import DESCENDING
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import os
import math
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

class PaginatedResponse(BaseModel):
    data: List[ESP32Response]
    pagination: Dict[str, Any]

class CountResponse(BaseModel):
    count: int

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

def apply_filters(readings, filters_dict):
    """Apply filters to readings array"""
    if not filters_dict:
        return readings
    
    filtered_readings = []
    for reading in readings:
        matches_all_filters = True
        
        for field, range_filter in filters_dict.items():
            if field not in reading:
                continue
                
            min_val = range_filter.get('min')
            max_val = range_filter.get('max')
            current_val = reading.get(field)
            
            if current_val is None:
                matches_all_filters = False
                break
                
            try:
                current_val_float = float(current_val)
                
                if min_val is not None and current_val_float < min_val:
                    matches_all_filters = False
                    break
                if max_val is not None and current_val_float > max_val:
                    matches_all_filters = False
                    break
                    
            except (ValueError, TypeError):
                matches_all_filters = False
                break
        
        if matches_all_filters:
            filtered_readings.append(reading)
    
    return filtered_readings

def apply_search(readings, search_query):
    """Apply search to readings array"""
    if not search_query:
        return readings
    
    search_query_lower = search_query.lower()
    filtered_readings = []
    
    for reading in readings:
        matches = False
        for key, value in reading.items():
            if key in ['_id', 'timestamp', 'device_id']:
                continue
            if value is not None and search_query_lower in str(value).lower():
                matches = True
                break
        if matches:
            filtered_readings.append(reading)
    
    return filtered_readings

def filter_readings_by_date_range(readings, start_date_str, end_date_str):
    """Filter readings by date range"""
    if not start_date_str or not end_date_str:
        return readings
    
    try:
        start_datetime = datetime.fromisoformat(start_date_str)
        end_datetime = datetime.fromisoformat(end_date_str)
        end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
        
        filtered_readings = []
        for reading in readings:
            timestamp = convert_firebase_timestamp(reading.get("timestamp", {}))
            if start_datetime <= timestamp <= end_datetime:
                filtered_readings.append(reading)
        
        return filtered_readings
    except Exception as e:
        print(f"Error filtering by date range: {e}")
        return readings

# API endpoints with pagination
@router.get("/esp32-1", response_model=PaginatedResponse)
async def get_esp32_1_data(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    sortBy: str = Query("timestamp"),
    sortOrder: str = Query("desc"),
    filters: str = Query(None)
):
    try:
        db = await get_database()
        # Get the esp32-1 document which contains the readings array
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return {
                "data": [],
                "pagination": {
                    "currentPage": 1,
                    "totalPages": 0,
                    "totalItems": 0,
                    "itemsPerPage": limit,
                    "hasNextPage": False,
                    "hasPrevPage": False
                }
            }
        
        # Get all readings
        all_readings = doc["readings"]
        
        # Apply search if provided
        if search:
            all_readings = apply_search(all_readings, search)
        
        # Apply filters if provided
        if filters:
            try:
                filters_dict = eval(filters)  # Convert string to dict
                all_readings = apply_filters(all_readings, filters_dict)
            except:
                pass  # If filters are invalid, ignore them
        
        # Sort readings
        reverse = sortOrder.lower() == "desc"
        
        if sortBy == "timestamp":
            all_readings.sort(key=lambda x: convert_firebase_timestamp(x.get("timestamp", {})), reverse=reverse)
        else:
            # Sort by other fields
            def get_sort_value(reading):
                value = reading.get(sortBy)
                try:
                    return float(value) if value is not None else (float('-inf') if reverse else float('inf'))
                except (ValueError, TypeError):
                    return "" if reverse else "zzzz"  # Put invalid values at end
            
            all_readings.sort(key=get_sort_value, reverse=reverse)
        
        # Calculate pagination
        total_items = len(all_readings)
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
        skip = (page - 1) * limit
        
        # Get paginated slice
        paginated_readings = all_readings[skip:skip + limit]
        
        # Process the paginated readings
        results = []
        for reading in paginated_readings:
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
        
        return {
            "data": results,
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalItems": total_items,
                "itemsPerPage": limit,
                "hasNextPage": page < total_pages,
                "hasPrevPage": page > 1
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ESP32-1 data: {str(e)}")

@router.get("/esp32-2", response_model=PaginatedResponse)
async def get_esp32_2_data(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    sortBy: str = Query("timestamp"),
    sortOrder: str = Query("desc"),
    filters: str = Query(None)
):
    try:
        db = await get_database()
        # Get the esp32-2 document which contains the readings array
        doc = await db.sensor_readings.find_one({"_id": "esp32-2"})
        
        if not doc or "readings" not in doc:
            return {
                "data": [],
                "pagination": {
                    "currentPage": 1,
                    "totalPages": 0,
                    "totalItems": 0,
                    "itemsPerPage": limit,
                    "hasNextPage": False,
                    "hasPrevPage": False
                }
            }
        
        # Get all readings
        all_readings = doc["readings"]
        
        # Apply search if provided
        if search:
            all_readings = apply_search(all_readings, search)
        
        # Apply filters if provided
        if filters:
            try:
                filters_dict = eval(filters)  # Convert string to dict
                all_readings = apply_filters(all_readings, filters_dict)
            except:
                pass  # If filters are invalid, ignore them
        
        # Sort readings
        reverse = sortOrder.lower() == "desc"
        
        if sortBy == "timestamp":
            all_readings.sort(key=lambda x: convert_firebase_timestamp(x.get("timestamp", {})), reverse=reverse)
        else:
            # Sort by other fields
            def get_sort_value(reading):
                value = reading.get(sortBy)
                try:
                    return float(value) if value is not None else (float('-inf') if reverse else float('inf'))
                except (ValueError, TypeError):
                    return "" if reverse else "zzzz"  # Put invalid values at end
            
            all_readings.sort(key=get_sort_value, reverse=reverse)
        
        # Calculate pagination
        total_items = len(all_readings)
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
        skip = (page - 1) * limit
        
        # Get paginated slice
        paginated_readings = all_readings[skip:skip + limit]
        
        # Process the paginated readings
        results = []
        for reading in paginated_readings:
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
        
        return {
            "data": results,
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalItems": total_items,
                "itemsPerPage": limit,
                "hasNextPage": page < total_pages,
                "hasPrevPage": page > 1
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ESP32-2 data: {str(e)}")

# Date range endpoints for printing
@router.get("/esp32-1/range", response_model=List[ESP32Response])
async def get_esp32_1_date_range(
    startDate: str,
    endDate: str,
    sortBy: str = Query("timestamp"),
    sortOrder: str = Query("desc")
):
    """Get ESP32-1 data for a specific date range"""
    try:
        print(f"📅 ESP32-1 Range Request: {startDate} to {endDate}")
        
        db = await get_database()
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            print("❌ No ESP32-1 document or readings found")
            return []
        
        print(f"📊 Total readings in ESP32-1: {len(doc['readings'])}")
        
        # Filter readings by date range
        filtered_readings = filter_readings_by_date_range(doc["readings"], startDate, endDate)
        
        print(f"✅ Filtered readings count: {len(filtered_readings)}")
        
        # Sort readings
        reverse = sortOrder.lower() == "desc"
        
        if sortBy == "timestamp":
            filtered_readings.sort(key=lambda x: convert_firebase_timestamp(x.get("timestamp", {})), reverse=reverse)
        else:
            def get_sort_value(reading):
                value = reading.get(sortBy)
                try:
                    return float(value) if value is not None else (float('-inf') if reverse else float('inf'))
                except (ValueError, TypeError):
                    return "" if reverse else "zzzz"
            
            filtered_readings.sort(key=get_sort_value, reverse=reverse)
        
        # Process the filtered readings
        results = []
        for reading in filtered_readings:
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
        
        print(f"🎯 Returning {len(results)} processed records")
        return results
        
    except Exception as e:
        print(f"❌ Error in ESP32-1 range endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching ESP32-1 range data: {str(e)}")

@router.get("/esp32-2/range", response_model=List[ESP32Response])
async def get_esp32_2_date_range(
    startDate: str,
    endDate: str,
    sortBy: str = Query("timestamp"),
    sortOrder: str = Query("desc")
):
    """Get ESP32-2 data for a specific date range"""
    try:
        db = await get_database()
        doc = await db.sensor_readings.find_one({"_id": "esp32-2"})
        
        if not doc or "readings" not in doc:
            return []
        
        # Filter readings by date range
        filtered_readings = filter_readings_by_date_range(doc["readings"], startDate, endDate)
        
        # Sort readings
        reverse = sortOrder.lower() == "desc"
        
        if sortBy == "timestamp":
            filtered_readings.sort(key=lambda x: convert_firebase_timestamp(x.get("timestamp", {})), reverse=reverse)
        else:
            def get_sort_value(reading):
                value = reading.get(sortBy)
                try:
                    return float(value) if value is not None else (float('-inf') if reverse else float('inf'))
                except (ValueError, TypeError):
                    return "" if reverse else "zzzz"
            
            filtered_readings.sort(key=get_sort_value, reverse=reverse)
        
        # Process the filtered readings
        results = []
        for reading in filtered_readings:
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
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ESP32-2 range data: {str(e)}")

# Count endpoints for record estimation
@router.get("/esp32-1/count", response_model=CountResponse)
async def get_esp32_1_count(
    startDate: str = Query(None),
    endDate: str = Query(None)
):
    """Get count of ESP32-1 records for a date range"""
    try:
        db = await get_database()
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return {"count": 0}
        
        if startDate and endDate:
            # Filter by date range and count
            filtered_readings = filter_readings_by_date_range(doc["readings"], startDate, endDate)
            return {"count": len(filtered_readings)}
        else:
            # Return total count
            return {"count": len(doc["readings"])}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting ESP32-1 records: {str(e)}")

@router.get("/esp32-2/count", response_model=CountResponse)
async def get_esp32_2_count(
    startDate: str = Query(None),
    endDate: str = Query(None)
):
    """Get count of ESP32-2 records for a date range"""
    try:
        db = await get_database()
        doc = await db.sensor_readings.find_one({"_id": "esp32-2"})
        
        if not doc or "readings" not in doc:
            return {"count": 0}
        
        if startDate and endDate:
            # Filter by date range and count
            filtered_readings = filter_readings_by_date_range(doc["readings"], startDate, endDate)
            return {"count": len(filtered_readings)}
        else:
            # Return total count
            return {"count": len(doc["readings"])}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting ESP32-2 records: {str(e)}")

# Export endpoints (get all data without pagination)
@router.get("/esp32-1/all", response_model=List[ESP32Response])
async def get_all_esp32_1_data(
    sortBy: str = Query("timestamp"),
    sortOrder: str = Query("desc")
):
    """Get all ESP32-1 data for exports"""
    try:
        db = await get_database()
        doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        
        if not doc or "readings" not in doc:
            return []
        
        all_readings = doc["readings"]
        
        # Sort readings
        reverse = sortOrder.lower() == "desc"
        
        if sortBy == "timestamp":
            all_readings.sort(key=lambda x: convert_firebase_timestamp(x.get("timestamp", {})), reverse=reverse)
        else:
            def get_sort_value(reading):
                value = reading.get(sortBy)
                try:
                    return float(value) if value is not None else (float('-inf') if reverse else float('inf'))
                except (ValueError, TypeError):
                    return "" if reverse else "zzzz"
            
            all_readings.sort(key=get_sort_value, reverse=reverse)
        
        results = []
        for reading in all_readings:
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
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all ESP32-1 data: {str(e)}")

@router.get("/esp32-2/all", response_model=List[ESP32Response])
async def get_all_esp32_2_data(
    sortBy: str = Query("timestamp"),
    sortOrder: str = Query("desc")
):
    """Get all ESP32-2 data for exports"""
    try:
        db = await get_database()
        doc = await db.sensor_readings.find_one({"_id": "esp32-2"})
        
        if not doc or "readings" not in doc:
            return []
        
        all_readings = doc["readings"]
        
        # Sort readings
        reverse = sortOrder.lower() == "desc"
        
        if sortBy == "timestamp":
            all_readings.sort(key=lambda x: convert_firebase_timestamp(x.get("timestamp", {})), reverse=reverse)
        else:
            def get_sort_value(reading):
                value = reading.get(sortBy)
                try:
                    return float(value) if value is not None else (float('-inf') if reverse else float('inf'))
                except (ValueError, TypeError):
                    return "" if reverse else "zzzz"
            
            all_readings.sort(key=get_sort_value, reverse=reverse)
        
        results = []
        for reading in all_readings:
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
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all ESP32-2 data: {str(e)}")

# Global search endpoint (updated with pagination)
@router.get("/global-search", response_model=PaginatedResponse)
async def global_search(
    query: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    try:
        db = await get_database()
        all_results = []
        
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
                    
                    all_results.append(device_data)
        
        # Sort by timestamp descending
        all_results.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Calculate pagination
        total_items = len(all_results)
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
        skip = (page - 1) * limit
        
        # Get paginated slice
        paginated_results = all_results[skip:skip + limit]
        
        return {
            "data": paginated_results,
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalItems": total_items,
                "itemsPerPage": limit,
                "hasNextPage": page < total_pages,
                "hasPrevPage": page > 1
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing global search: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = await get_database()
        
        # Check if both collections exist and have data
        esp32_1_doc = await db.sensor_readings.find_one({"_id": "esp32-1"})
        esp32_2_doc = await db.sensor_readings.find_one({"_id": "esp32-2"})
        
        esp32_1_count = len(esp32_1_doc.get("readings", [])) if esp32_1_doc else 0
        esp32_2_count = len(esp32_2_doc.get("readings", [])) if esp32_2_doc else 0
        
        return {
            "status": "healthy",
            "database": "connected",
            "esp32_1_records": esp32_1_count,
            "esp32_2_records": esp32_2_count,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")