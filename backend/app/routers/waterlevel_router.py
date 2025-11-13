# from fastapi import APIRouter, HTTPException, Query, Depends
# from datetime import datetime, timedelta
# from typing import List, Optional, Any
# from bson import ObjectId
# from pydantic import BaseModel, Field

# from app.services.database import get_database

# router = APIRouter(prefix="/api/water-level", tags=["water-level"])

# class WaterLevelReading(BaseModel):
#     device_id: str = Field(..., description="Device identifier")
#     waterLevel: float = Field(..., ge=0, le=100, description="Water level percentage")
#     timestamp: Optional[datetime] = Field(None, description="Reading timestamp")

# class WaterLevelResponse(BaseModel):
#     id: str = Field(..., description="Document ID")
#     device_id: str = Field(..., description="Device identifier")
#     waterLevel: float = Field(..., ge=0, le=100, description="Water level percentage")
#     timestamp: Optional[datetime] = Field(None, description="Reading timestamp")

# class WaterLevelStats(BaseModel):
#     min: float
#     max: float
#     avg: float
#     count: int
#     time_period_hours: int

# def convert_firestore_timestamp(timestamp_data: Any) -> datetime:
#     """Convert Firestore-style timestamp to Python datetime"""
#     if isinstance(timestamp_data, datetime):
#         return timestamp_data
    
#     if isinstance(timestamp_data, dict):
#         if '_seconds' in timestamp_data:
#             # Firestore timestamp format
#             seconds = timestamp_data['_seconds']
#             nanoseconds = timestamp_data.get('_nanoseconds', 0)
#             return datetime.fromtimestamp(seconds + nanoseconds / 1e9)
#         elif 'seconds' in timestamp_data:
#             # Alternative Firestore format
#             seconds = timestamp_data['seconds']
#             nanoseconds = timestamp_data.get('nanoseconds', 0)
#             return datetime.fromtimestamp(seconds + nanoseconds / 1e9)
    
#     # If it's already a string or other format, try to parse it
#     try:
#         return datetime.fromisoformat(str(timestamp_data))
#     except (ValueError, TypeError):
#         # Fallback to current time if parsing fails
#         return datetime.now()

# @router.get("/readings", response_model=List[WaterLevelResponse])
# async def get_water_level_readings(
#     skip: int = Query(0, ge=0),
#     device_id: Optional[str] = None,
#     db=Depends(get_database)
# ):
#     """
#     Get water level readings with optional filtering
#     """
#     try:
#         query = {}
#         if device_id:
#             query["device_id"] = device_id
            
#         # Remove the limit to fetch all data
#         readings = await db["water_level_readings"].find(
#             query, 
#             sort=[("timestamp", -1)]
#         ).skip(skip).to_list(length=None)  # length=None returns all documents
        
#         # Convert the data to the expected format
#         processed_readings = []
#         for reading in readings:
#             # Convert ObjectId to string
#             reading_id = str(reading.get('_id', ''))
            
#             # Convert Firestore timestamp to datetime
#             timestamp = convert_firestore_timestamp(reading.get('timestamp'))
            
#             processed_readings.append({
#                 "id": reading_id,
#                 "device_id": reading.get('device_id', ''),
#                 "waterLevel": reading.get('waterLevel', 0.0),
#                 "timestamp": timestamp
#             })
        
#         return processed_readings
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching readings: {str(e)}")

# @router.get("/readings/{reading_id}", response_model=WaterLevelResponse)
# async def get_water_level_reading(reading_id: str, db=Depends(get_database)):
#     """
#     Get a specific water level reading by ID
#     """
#     try:
#         if not ObjectId.is_valid(reading_id):
#             raise HTTPException(status_code=400, detail="Invalid reading ID format")
            
#         reading = await db["water_level_readings"].find_one({"_id": ObjectId(reading_id)})
#         if not reading:
#             raise HTTPException(status_code=404, detail="Reading not found")
        
#         # Convert the data to the expected format
#         timestamp = convert_firestore_timestamp(reading.get('timestamp'))
        
#         return WaterLevelResponse(
#             id=str(reading['_id']),
#             device_id=reading.get('device_id', ''),
#             waterLevel=reading.get('waterLevel', 0.0),
#             timestamp=timestamp
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching reading: {str(e)}")

# @router.get("/latest", response_model=List[WaterLevelResponse])
# async def get_latest_water_level_readings(
#     limit: int = Query(10, ge=1, le=50),
#     device_id: Optional[str] = None,
#     db=Depends(get_database)
# ):
#     """
#     Get the latest water level readings
#     """
#     try:
#         query = {}
#         if device_id:
#             query["device_id"] = device_id
            
#         # Get readings from the last 5 minutes
#         five_minutes_ago = datetime.now() - timedelta(minutes=5)
#         query["timestamp"] = {"$gte": five_minutes_ago}
        
#         readings = await db["water_level_readings"].find(
#             query, 
#             sort=[("timestamp", -1)]
#         ).limit(limit).to_list(length=limit)
        
#         # Convert the data to the expected format
#         processed_readings = []
#         for reading in readings:
#             # Convert ObjectId to string
#             reading_id = str(reading.get('_id', ''))
            
#             # Convert Firestore timestamp to datetime
#             timestamp = convert_firestore_timestamp(reading.get('timestamp'))
            
#             processed_readings.append({
#                 "id": reading_id,
#                 "device_id": reading.get('device_id', ''),
#                 "waterLevel": reading.get('waterLevel', 0.0),
#                 "timestamp": timestamp
#             })
        
#         return processed_readings
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching latest readings: {str(e)}")

# @router.post("/readings", response_model=WaterLevelResponse)
# async def create_water_level_reading(reading: WaterLevelReading, db=Depends(get_database)):
#     """
#     Create a new water level reading
#     """
#     try:
#         reading_dict = reading.dict()
#         # Use provided timestamp or current time if not provided
#         if not reading_dict.get("timestamp"):
#             reading_dict["timestamp"] = datetime.now()
        
#         result = await db["water_level_readings"].insert_one(reading_dict)
#         created_reading = await db["water_level_readings"].find_one({"_id": result.inserted_id})
        
#         # Convert the data to the expected format
#         timestamp = convert_firestore_timestamp(created_reading.get('timestamp'))
        
#         return WaterLevelResponse(
#             id=str(created_reading['_id']),
#             device_id=created_reading.get('device_id', ''),
#             waterLevel=created_reading.get('waterLevel', 0.0),
#             timestamp=timestamp
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error creating reading: {str(e)}")

# @router.get("/stats", response_model=WaterLevelStats)
# async def get_water_level_stats(
#     device_id: Optional[str] = None,
#     hours: int = Query(24, ge=1, le=168),  # Default to 24 hours, max 1 week
#     db=Depends(get_database)
# ):
#     """
#     Get statistics for water level readings
#     """
#     try:
#         query = {}
#         if device_id:
#             query["device_id"] = device_id
            
#         # Get readings from the specified time period
#         time_threshold = datetime.now() - timedelta(hours=hours)
#         query["timestamp"] = {"$gte": time_threshold}
        
#         pipeline = [
#             {"$match": query},
#             {"$group": {
#                 "_id": None,
#                 "min": {"$min": "$waterLevel"},
#                 "max": {"$max": "$waterLevel"},
#                 "avg": {"$avg": "$waterLevel"},
#                 "count": {"$sum": 1}
#             }}
#         ]
        
#         stats = await db["water_level_readings"].aggregate(pipeline).to_list(length=1)
        
#         if stats and stats[0]:
#             return WaterLevelStats(
#                 min=stats[0].get("min", 0),
#                 max=stats[0].get("max", 0),
#                 avg=stats[0].get("avg", 0),
#                 count=stats[0].get("count", 0),
#                 time_period_hours=hours
#             )
#         else:
#             return WaterLevelStats(
#                 min=0,
#                 max=0,
#                 avg=0,
#                 count=0,
#                 time_period_hours=hours
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

# @router.get("/device/{device_id}/latest", response_model=WaterLevelResponse)
# async def get_latest_reading_by_device(device_id: str, db=Depends(get_database)):
#     """
#     Get the latest reading for a specific device
#     """
#     try:
#         reading = await db["water_level_readings"].find_one(
#             {"device_id": device_id},
#             sort=[("timestamp", -1)]
#         )
        
#         if not reading:
#             raise HTTPException(status_code=404, detail="No readings found for this device")
        
#         # Convert the data to the expected format
#         timestamp = convert_firestore_timestamp(reading.get('timestamp'))
        
#         return WaterLevelResponse(
#             id=str(reading['_id']),
#             device_id=reading.get('device_id', ''),
#             waterLevel=reading.get('waterLevel', 0.0),
#             timestamp=timestamp
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching latest reading: {str(e)}")


from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId
from app.services.database import get_database

router = APIRouter(prefix="/api/water-level", tags=["water-level"])

# Pydantic models
class WaterLevelReadingResponse(BaseModel):
    id: str
    device_id: str
    waterLevel: float
    timestamp: datetime

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class WaterLevelStats(BaseModel):
    average: float
    min: float
    max: float

class StatsResponse(BaseModel):
    waterLevel: WaterLevelStats
    total_readings: int

class PaginatedResponse(BaseModel):
    data: List[WaterLevelReadingResponse]
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
def water_level_reading_helper(reading, device_id, index=None) -> dict:
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
        "waterLevel": reading.get("waterLevel", 0),
        "timestamp": timestamp,
        "timestamp_ms": timestamp_ms,  # For accurate sorting
    }

@router.get("/readings", response_model=PaginatedResponse)
async def get_water_level_readings(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query for device_id"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering")
):
    """
    Get paginated water level readings, sorted by timestamp (newest first)
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        # Build query for filtering
        query = {}
        if search:
            query["device_id"] = {"$regex": search, "$options": "i"}
        
        # Apply date filtering if specified
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["timestamp"] = date_query
        
        # Get total count for pagination
        total_items = await collection.count_documents(query)
        
        # Get paginated data
        readings = await collection.find(
            query, 
            sort=[("timestamp", -1)]
        ).skip((page - 1) * limit).limit(limit).to_list(length=limit)
        
        # Process readings for response
        processed_readings = []
        for i, reading in enumerate(readings):
            device_id = reading.get("device_id", "unknown")
            response_reading = water_level_reading_helper(reading, device_id, i)
            processed_readings.append(response_reading)
        
        # Remove the temporary timestamp_ms field before returning
        for reading in processed_readings:
            reading.pop('timestamp_ms', None)
        
        # Calculate pagination info
        total_pages = (total_items + limit - 1) // limit  # Ceiling division
        
        return {
            "data": processed_readings,
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
        raise HTTPException(status_code=500, detail=f"Error fetching water level data: {str(e)}")

@router.get("/readings/all", response_model=List[WaterLevelReadingResponse])
async def get_all_water_level_readings(
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering")
):
    """
    Get ALL water level readings (use with caution for large datasets)
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        # Build query for filtering
        query = {}
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["timestamp"] = date_query
        
        # Get all data
        readings = await collection.find(
            query, 
            sort=[("timestamp", -1)]
        ).to_list(length=None)
        
        # Process readings for response
        processed_readings = []
        for i, reading in enumerate(readings):
            device_id = reading.get("device_id", "unknown")
            response_reading = water_level_reading_helper(reading, device_id, i)
            processed_readings.append(response_reading)
        
        # Remove timestamp_ms field
        for reading in processed_readings:
            reading.pop('timestamp_ms', None)
        
        return processed_readings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all water level data: {str(e)}")

@router.get("/readings/recent", response_model=PaginatedResponse)
async def get_recent_water_level_readings(
    hours: int = Query(24, ge=1, le=168),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get recent water level readings with pagination
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        # Calculate time threshold
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        # Build query for recent readings
        query = {
            "timestamp": {"$gte": time_threshold}
        }
        
        # Get total count for pagination
        total_items = await collection.count_documents(query)
        
        # Get paginated data
        readings = await collection.find(
            query, 
            sort=[("timestamp", -1)]
        ).skip((page - 1) * limit).limit(limit).to_list(length=limit)
        
        # Process readings for response
        processed_readings = []
        for i, reading in enumerate(readings):
            device_id = reading.get("device_id", "unknown")
            response_reading = water_level_reading_helper(reading, device_id, i)
            processed_readings.append(response_reading)
        
        # Remove timestamp_ms field
        for reading in processed_readings:
            reading.pop('timestamp_ms', None)
        
        # Calculate pagination info
        total_pages = (total_items + limit - 1) // limit
        
        return {
            "data": processed_readings,
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
        raise HTTPException(status_code=500, detail=f"Error fetching recent water level data: {str(e)}")

@router.get("/stats", response_model=StatsResponse)
async def get_water_level_stats(
    hours: Optional[int] = Query(None, description="Time window in hours for statistics"),
    start_date: Optional[datetime] = Query(None, description="Start date for statistics"),
    end_date: Optional[datetime] = Query(None, description="End date for statistics")
):
    """
    Get statistics for water level readings
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        # Build query based on time filtering
        query = {}
        
        if hours:
            time_threshold = datetime.now() - timedelta(hours=hours)
            query["timestamp"] = {"$gte": time_threshold}
        elif start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["timestamp"] = date_query
        
        # Get filtered readings
        readings = await collection.find(query).to_list(length=None)
        
        # Extract water level values with validation
        water_levels = []
        for reading in readings:
            water_level = reading.get("waterLevel")
            if water_level is not None:
                try:
                    water_levels.append(float(water_level))
                except (ValueError, TypeError):
                    pass
        
        # Calculate statistics only if we have valid data
        if water_levels:
            return StatsResponse(
                waterLevel=WaterLevelStats(
                    average=round(sum(water_levels) / len(water_levels), 2),
                    min=round(min(water_levels), 2),
                    max=round(max(water_levels), 2)
                ),
                total_readings=len(water_levels)
            )
        
        return StatsResponse(
            waterLevel=WaterLevelStats(average=0, min=0, max=0),
            total_readings=0
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

@router.get("/count")
async def get_readings_count():
    """
    Get total count of water level readings
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        count = await collection.count_documents({})
        return {"count": count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting readings: {str(e)}")

@router.get("/test-document")
async def test_document():
    """
    Test endpoint to check water level documents structure
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        # Get a sample document
        document = await collection.find_one()
        
        if document:
            # Get total count
            total_count = await collection.count_documents({})
            
            # Sample a few readings to examine structure
            sample_readings = await collection.find().limit(3).to_list(length=3)
            
            return {
                "exists": True,
                "total_count": total_count,
                "document_keys": list(document.keys()) if document else [],
                "sample_readings": sample_readings
            }
        else:
            # Check what collections exist
            collections = await db.list_collection_names()
            return {
                "exists": False,
                "collections": collections
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing document: {str(e)}")

@router.get("/readings/raw")
async def get_raw_readings_sample(limit: int = 5):
    """
    Return a raw sample (first `limit`) of water level readings without any processing.
    Useful for debugging timestamp shapes and payload structure.
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        readings = await collection.find().limit(limit).to_list(length=limit)
        total_count = await collection.count_documents({})
        
        return {
            "total_count": total_count,
            "sample_count": len(readings),
            "sample": readings
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error returning raw readings sample: {str(e)}")

@router.get("/readings/range", response_model=List[WaterLevelReadingResponse])
async def get_water_level_data_range(
    from_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get ALL water level readings within a specific date range (no pagination)
    """
    try:
        print(f"📅 Range endpoint called: {from_date} to {to_date}")
        
        # Parse and validate dates
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)  # Include the entire end day

        db = await get_database()
        collection = db.water_level_readings
        
        print(f"🔍 Querying database: {from_datetime} to {to_datetime}")
        
        # Build date range query
        query = {
            "timestamp": {
                "$gte": from_datetime,
                "$lt": to_datetime
            }
        }
        
        # Debug: Check what's in the collection first
        total_count = await collection.count_documents({})
        print(f"📊 Total documents in collection: {total_count}")
        
        # Get matching documents
        cursor = collection.find(query).sort("timestamp", -1)
        readings = await cursor.to_list(length=None)
        
        print(f"✅ Found {len(readings)} documents matching query")
        
        # Process readings for response
        processed_readings = []
        for i, reading in enumerate(readings):
            print(f"📖 Processing reading {i}: {reading}")
            device_id = reading.get("device_id", "unknown")
            processed_reading = water_level_reading_helper(reading, device_id, i)
            processed_readings.append(processed_reading)
        
        print(f"🎯 Returning {len(processed_readings)} processed readings")
        
        # Return empty array if no data found (not an error)
        return processed_readings
        
    except ValueError as ve:
        print(f"❌ ValueError: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(ve)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching date range data: {str(e)}"
        )

@router.post("/readings", response_model=WaterLevelReadingResponse)
async def create_water_level_reading(reading_data: dict):
    """
    Create a new water level reading
    """
    try:
        db = await get_database()
        collection = db.water_level_readings
        
        # Validate required fields
        if "device_id" not in reading_data or "waterLevel" not in reading_data:
            raise HTTPException(
                status_code=400,
                detail="device_id and waterLevel are required fields"
            )
        
        # Add timestamp if not provided
        if "timestamp" not in reading_data:
            reading_data["timestamp"] = datetime.now()
        
        # Insert the reading
        result = await collection.insert_one(reading_data)
        
        # Retrieve the created document
        created_reading = await collection.find_one({"_id": result.inserted_id})
        
        # Convert to response format
        device_id = created_reading.get("device_id", "unknown")
        response_reading = water_level_reading_helper(created_reading, device_id)
        response_reading.pop('timestamp_ms', None)
        
        return response_reading
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating reading: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = await get_database()
        # Try to ping the database
        await db.command('ping')
        
        # Check water level collection
        collection = db.water_level_readings
        count = await collection.count_documents({})
        
        return {
            "status": "healthy", 
            "database": "connected",
            "water_level_readings_count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Make sure the router is exported
__all__ = ["router"]