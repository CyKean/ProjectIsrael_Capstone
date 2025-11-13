# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
# from fastapi.responses import JSONResponse
# from datetime import datetime, timedelta
# from typing import List, Optional
# from pydantic import BaseModel
# from bson import ObjectId
# import json

# # Import your MongoDB connection and models
# from app.services.database import get_database

# router = APIRouter(prefix="/api/soil-moisture", tags=["soil-moisture"])

# # Pydantic models
# class SoilMoistureReadingResponse(BaseModel):
#     id: str
#     soilMoisture: float
#     timestamp: datetime
#     deviceId: Optional[str] = None

# class SoilMoistureCreate(BaseModel):
#     soilMoisture: float
#     deviceId: Optional[str] = None
#     timestamp: Optional[datetime] = None

# # WebSocket connections store
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def broadcast(self, message: dict):
#         for connection in self.active_connections:
#             try:
#                 await connection.send_json(message)
#             except:
#                 self.disconnect(connection)

# manager = ConnectionManager()

# @router.get("", response_model=List[SoilMoistureReadingResponse])
# async def get_soil_moisture_readings(
#     device_id: Optional[str] = None
# ):
#     """
#     Get ALL soil moisture readings from the sensor_readings collection
#     with the nested structure: {_id: "esp32-2", readings: [...]}
#     Returns all available readings without any limit
#     """
#     try:
#         db = await get_database()
#         collection = db["sensor_readings"]
        
#         # Find the document with the specific device ID
#         query = {"_id": "esp32-2"}  # Fixed device ID based on your structure
        
#         # Get the document containing the readings array
#         device_doc = await collection.find_one(query)
        
#         if not device_doc or "readings" not in device_doc:
#             return []
        
#         # Extract and process ALL readings
#         readings = device_doc["readings"]
        
#         # Filter and sort readings
#         filtered_readings = []
#         for reading in readings:
#             # Only include readings that have soilMoisture data
#             if "soilMoisture" in reading and reading["soilMoisture"] is not None:
#                 # Convert Firestore timestamp to datetime
#                 if "timestamp" in reading and "_seconds" in reading["timestamp"]:
#                     timestamp = datetime.fromtimestamp(reading["timestamp"]["_seconds"])
#                 else:
#                     # Fallback to current time if no timestamp
#                     timestamp = datetime.utcnow()
                
#                 filtered_readings.append({
#                     "id": reading.get("_id", str(ObjectId())),
#                     "soilMoisture": reading["soilMoisture"],
#                     "timestamp": timestamp,
#                     "deviceId": reading.get("device_id", "esp32-2")
#                 })
        
#         # Sort by timestamp descending (newest first)
#         filtered_readings.sort(key=lambda x: x["timestamp"], reverse=True)
        
#         print(f"📊 Returning ALL {len(filtered_readings)} soil moisture readings (no limit)")
#         return filtered_readings
        
#     except Exception as e:
#         print(f"❌ Error fetching soil moisture readings: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error fetching soil moisture readings: {str(e)}")

# @router.get("/test")
# async def test_endpoint():
#     """
#     Test endpoint to verify the API is working and check database connection
#     """
#     try:
#         db = await get_database()
#         collection = db["sensor_readings"]
        
#         # Check if the document exists
#         device_doc = await collection.find_one({"_id": "esp32-2"})
        
#         if not device_doc:
#             return {
#                 "status": "error",
#                 "message": "Document with _id 'esp32-2' not found",
#                 "document_exists": False
#             }
        
#         # Count readings with soilMoisture data
#         readings_count = len(device_doc.get("readings", []))
#         soil_moisture_count = sum(1 for r in device_doc.get("readings", []) if "soilMoisture" in r)
        
#         # Get sample reading
#         sample_reading = None
#         for reading in device_doc.get("readings", []):
#             if "soilMoisture" in reading:
#                 sample_reading = reading
#                 break
        
#         return {
#             "status": "success",
#             "message": "API is working correctly",
#             "database_connected": True,
#             "document_exists": True,
#             "total_readings": readings_count,
#             "soil_moisture_readings": soil_moisture_count,
#             "sample_reading": sample_reading
#         }
        
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": f"Database connection failed: {str(e)}",
#             "database_connected": False
#         }

# @router.post("")
# async def create_soil_moisture_reading(reading: SoilMoistureCreate):
#     """
#     Create a new soil moisture reading - updated for your nested structure
#     """
#     try:
#         db = await get_database()
#         collection = db["sensor_readings"]
        
#         # Prepare the new reading document
#         new_reading = {
#             "_id": str(ObjectId()),
#             "device_id": reading.deviceId or "esp32-2",
#             "soilMoisture": reading.soilMoisture,
#             "timestamp": {
#                 "_seconds": int((reading.timestamp or datetime.utcnow()).timestamp()),
#                 "_nanoseconds": 0
#             }
#         }
        
#         # Add optional fields if they exist in the original structure
#         if hasattr(reading, 'temperature'):
#             new_reading["temperature"] = reading.temperature
#         if hasattr(reading, 'humidity'):
#             new_reading["humidity"] = reading.humidity
        
#         # Update the document by pushing the new reading to the readings array
#         result = await collection.update_one(
#             {"_id": "esp32-2"},
#             {"$push": {"readings": new_reading}},
#             upsert=True  # Create the document if it doesn't exist
#         )
        
#         # Broadcast to WebSocket clients
#         broadcast_data = {
#             "soilMoisture": reading.soilMoisture,
#             "deviceId": reading.deviceId or "esp32-2",
#             "timestamp": reading.timestamp or datetime.utcnow()
#         }
#         await manager.broadcast(broadcast_data)
        
#         return {"id": new_reading["_id"], "message": "Reading created successfully"}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error creating soil moisture reading: {str(e)}")

# @router.get("/stats")
# async def get_soil_moisture_stats(
#     device_id: Optional[str] = None,
#     hours: int = 24
# ):
#     """
#     Get statistics for soil moisture readings from the nested structure
#     """
#     try:
#         db = await get_database()
#         collection = db["sensor_readings"]
        
#         # Find the document
#         device_doc = await collection.find_one({"_id": "esp32-2"})
        
#         if not device_doc or "readings" not in device_doc:
#             return {
#                 "min": 0,
#                 "max": 0,
#                 "avg": 0,
#                 "count": 0
#             }
        
#         # Calculate time range
#         start_time = datetime.utcnow() - timedelta(hours=hours)
#         start_timestamp_seconds = int(start_time.timestamp())
        
#         # Filter readings by time and extract soil moisture values
#         values = []
#         for reading in device_doc["readings"]:
#             if "soilMoisture" in reading and reading["soilMoisture"] is not None:
#                 # Check timestamp if available
#                 if ("timestamp" in reading and 
#                     "_seconds" in reading["timestamp"] and 
#                     reading["timestamp"]["_seconds"] >= start_timestamp_seconds):
#                     values.append(reading["soilMoisture"])
        
#         if not values:
#             return {
#                 "min": 0,
#                 "max": 0,
#                 "avg": 0,
#                 "count": 0
#             }
        
#         return {
#             "min": min(values),
#             "max": max(values),
#             "avg": sum(values) / len(values),
#             "count": len(values),
#             "latest": values[-1] if values else 0  # Most recent is last in array
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

# @router.websocket("/ws/soil-moisture")
# async def websocket_endpoint(websocket: WebSocket):
#     """
#     WebSocket endpoint for real-time soil moisture updates
#     """
#     await manager.connect(websocket)
#     try:
#         while True:
#             # Keep connection alive
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#     except Exception as e:
#         manager.disconnect(websocket)
#         print(f"WebSocket error: {e}")

# @router.get("/devices")
# async def get_available_devices():
#     """
#     Get list of available devices that have soil moisture readings
#     """
#     try:
#         db = await get_database()
#         collection = db["sensor_readings"]
        
#         # Since all readings are in one document, we return the fixed device ID
#         device_doc = await collection.find_one({"_id": "esp32-2"})
        
#         if device_doc:
#             return {"devices": ["esp32-2"]}
#         else:
#             return {"devices": []}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching devices: {str(e)}")

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId
import json
import math

# Import your MongoDB connection and models
from app.services.database import get_database

router = APIRouter(prefix="/api/soil-moisture", tags=["soil-moisture"])

# Pydantic models
class SoilMoistureReadingResponse(BaseModel):
    id: str
    soilMoisture: float
    timestamp: datetime
    deviceId: Optional[str] = None

class SoilMoistureCreate(BaseModel):
    soilMoisture: float
    deviceId: Optional[str] = None
    timestamp: Optional[datetime] = None

class PaginatedResponse(BaseModel):
    data: List[SoilMoistureReadingResponse]
    pagination: dict

# WebSocket connections store
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

@router.get("", response_model=PaginatedResponse)
async def get_soil_moisture_readings(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    device_id: Optional[str] = None
):
    """
    Get paginated soil moisture readings from the sensor_readings collection
    with the nested structure: {_id: "esp32-2", readings: [...]}
    Returns paginated results to prevent timeout with large datasets
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Find the document with the specific device ID
        query = {"_id": "esp32-2"}  # Fixed device ID based on your structure
        
        # Get the document containing the readings array
        device_doc = await collection.find_one(query)
        
        if not device_doc or "readings" not in device_doc:
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
        
        # Extract and process ALL readings first (for filtering)
        all_readings = device_doc["readings"]
        
        # Filter and process readings
        filtered_readings = []
        for reading in all_readings:
            # Only include readings that have soilMoisture data
            if "soilMoisture" in reading and reading["soilMoisture"] is not None:
                # Convert Firestore timestamp to datetime
                if "timestamp" in reading and "_seconds" in reading["timestamp"]:
                    timestamp = datetime.fromtimestamp(reading["timestamp"]["_seconds"])
                else:
                    # Fallback to current time if no timestamp
                    timestamp = datetime.utcnow()
                
                filtered_readings.append({
                    "id": reading.get("_id", str(ObjectId())),
                    "soilMoisture": reading["soilMoisture"],
                    "timestamp": timestamp,
                    "deviceId": reading.get("device_id", "esp32-2")
                })
        
        # Sort by timestamp descending (newest first)
        filtered_readings.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Calculate pagination
        total_items = len(filtered_readings)
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 0
        
        # Apply pagination
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_readings = filtered_readings[start_index:end_index]
        
        print(f"📊 Returning {len(paginated_readings)} soil moisture readings (Page {page}/{total_pages}, Total: {total_items})")
        
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
        print(f"❌ Error fetching soil moisture readings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching soil moisture readings: {str(e)}")

@router.get("/all", response_model=List[SoilMoistureReadingResponse])
async def get_all_soil_moisture_readings(
    device_id: Optional[str] = None
):
    """
    Get ALL soil moisture readings (use with caution for large datasets)
    This is the original endpoint kept for backward compatibility
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        query = {"_id": "esp32-2"}
        device_doc = await collection.find_one(query)
        
        if not device_doc or "readings" not in device_doc:
            return []
        
        readings = device_doc["readings"]
        
        filtered_readings = []
        for reading in readings:
            if "soilMoisture" in reading and reading["soilMoisture"] is not None:
                if "timestamp" in reading and "_seconds" in reading["timestamp"]:
                    timestamp = datetime.fromtimestamp(reading["timestamp"]["_seconds"])
                else:
                    timestamp = datetime.utcnow()
                
                filtered_readings.append({
                    "id": reading.get("_id", str(ObjectId())),
                    "soilMoisture": reading["soilMoisture"],
                    "timestamp": timestamp,
                    "deviceId": reading.get("device_id", "esp32-2")
                })
        
        filtered_readings.sort(key=lambda x: x["timestamp"], reverse=True)
        
        print(f"📊 Returning ALL {len(filtered_readings)} soil moisture readings (no limit)")
        return filtered_readings
        
    except Exception as e:
        print(f"❌ Error fetching all soil moisture readings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching soil moisture readings: {str(e)}")

@router.get("/search", response_model=PaginatedResponse)
async def search_soil_moisture_readings(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    min_moisture: Optional[float] = Query(None, ge=0, le=100, description="Minimum soil moisture"),
    max_moisture: Optional[float] = Query(None, ge=0, le=100, description="Maximum soil moisture"),
    device_id: Optional[str] = None
):
    """
    Search and filter soil moisture readings with pagination
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        query = {"_id": "esp32-2"}
        device_doc = await collection.find_one(query)
        
        if not device_doc or "readings" not in device_doc:
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
        
        # Extract and process readings with filtering
        all_readings = device_doc["readings"]
        filtered_readings = []
        
        for reading in all_readings:
            if "soilMoisture" in reading and reading["soilMoisture"] is not None:
                # Apply moisture filters
                if min_moisture is not None and reading["soilMoisture"] < min_moisture:
                    continue
                if max_moisture is not None and reading["soilMoisture"] > max_moisture:
                    continue
                
                # Convert timestamp
                if "timestamp" in reading and "_seconds" in reading["timestamp"]:
                    timestamp = datetime.fromtimestamp(reading["timestamp"]["_seconds"])
                else:
                    timestamp = datetime.utcnow()
                
                filtered_readings.append({
                    "id": reading.get("_id", str(ObjectId())),
                    "soilMoisture": reading["soilMoisture"],
                    "timestamp": timestamp,
                    "deviceId": reading.get("device_id", "esp32-2")
                })
        
        # Sort by timestamp descending
        filtered_readings.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Calculate pagination
        total_items = len(filtered_readings)
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 0
        
        # Apply pagination
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_readings = filtered_readings[start_index:end_index]
        
        print(f"🔍 Search results: {len(paginated_readings)} readings (Page {page}/{total_pages}, Total: {total_items})")
        
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
        print(f"❌ Error searching soil moisture readings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching soil moisture readings: {str(e)}")

@router.get("/test")
async def test_endpoint():
    """
    Test endpoint to verify the API is working and check database connection
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Check if the document exists
        device_doc = await collection.find_one({"_id": "esp32-2"})
        
        if not device_doc:
            return {
                "status": "error",
                "message": "Document with _id 'esp32-2' not found",
                "document_exists": False
            }
        
        # Count readings with soilMoisture data
        readings_count = len(device_doc.get("readings", []))
        soil_moisture_count = sum(1 for r in device_doc.get("readings", []) if "soilMoisture" in r)
        
        # Get sample reading
        sample_reading = None
        for reading in device_doc.get("readings", []):
            if "soilMoisture" in reading:
                sample_reading = reading
                break
        
        return {
            "status": "success",
            "message": "API is working correctly",
            "database_connected": True,
            "document_exists": True,
            "total_readings": readings_count,
            "soil_moisture_readings": soil_moisture_count,
            "sample_reading": sample_reading
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}",
            "database_connected": False
        }

@router.post("")
async def create_soil_moisture_reading(reading: SoilMoistureCreate):
    """
    Create a new soil moisture reading - updated for your nested structure
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Prepare the new reading document
        new_reading = {
            "_id": str(ObjectId()),
            "device_id": reading.deviceId or "esp32-2",
            "soilMoisture": reading.soilMoisture,
            "timestamp": {
                "_seconds": int((reading.timestamp or datetime.utcnow()).timestamp()),
                "_nanoseconds": 0
            }
        }
        
        # Add optional fields if they exist in the original structure
        if hasattr(reading, 'temperature'):
            new_reading["temperature"] = reading.temperature
        if hasattr(reading, 'humidity'):
            new_reading["humidity"] = reading.humidity
        
        # Update the document by pushing the new reading to the readings array
        result = await collection.update_one(
            {"_id": "esp32-2"},
            {"$push": {"readings": new_reading}},
            upsert=True  # Create the document if it doesn't exist
        )
        
        # Broadcast to WebSocket clients
        broadcast_data = {
            "soilMoisture": reading.soilMoisture,
            "deviceId": reading.deviceId or "esp32-2",
            "timestamp": reading.timestamp or datetime.utcnow()
        }
        await manager.broadcast(broadcast_data)
        
        return {"id": new_reading["_id"], "message": "Reading created successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating soil moisture reading: {str(e)}")

@router.get("/stats")
async def get_soil_moisture_stats(
    device_id: Optional[str] = None,
    hours: int = 24
):
    """
    Get statistics for soil moisture readings from the nested structure
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Find the document
        device_doc = await collection.find_one({"_id": "esp32-2"})
        
        if not device_doc or "readings" not in device_doc:
            return {
                "min": 0,
                "max": 0,
                "avg": 0,
                "count": 0
            }
        
        # Calculate time range
        start_time = datetime.utcnow() - timedelta(hours=hours)
        start_timestamp_seconds = int(start_time.timestamp())
        
        # Filter readings by time and extract soil moisture values
        values = []
        for reading in device_doc["readings"]:
            if "soilMoisture" in reading and reading["soilMoisture"] is not None:
                # Check timestamp if available
                if ("timestamp" in reading and 
                    "_seconds" in reading["timestamp"] and 
                    reading["timestamp"]["_seconds"] >= start_timestamp_seconds):
                    values.append(reading["soilMoisture"])
        
        if not values:
            return {
                "min": 0,
                "max": 0,
                "avg": 0,
                "count": 0
            }
        
        return {
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "count": len(values),
            "latest": values[-1] if values else 0  # Most recent is last in array
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

@router.websocket("/ws/soil-moisture")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time soil moisture updates
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket error: {e}")

@router.get("/devices")
async def get_available_devices():
    """
    Get list of available devices that have soil moisture readings
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Since all readings are in one document, we return the fixed device ID
        device_doc = await collection.find_one({"_id": "esp32-2"})
        
        if device_doc:
            return {"devices": ["esp32-2"]}
        else:
            return {"devices": []}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching devices: {str(e)}")

@router.get("/recent")
async def get_recent_soil_moisture_readings(
    limit: int = Query(50, ge=1, le=1000, description="Number of recent readings")
):
    """
    Get recent soil moisture readings for charts and real-time display
    This endpoint is optimized for chart data and real-time updates
    """
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        query = {"_id": "esp32-2"}
        device_doc = await collection.find_one(query)
        
        if not device_doc or "readings" not in device_doc:
            return []
        
        readings = device_doc["readings"]
        
        filtered_readings = []
        for reading in readings:
            if "soilMoisture" in reading and reading["soilMoisture"] is not None:
                if "timestamp" in reading and "_seconds" in reading["timestamp"]:
                    timestamp = datetime.fromtimestamp(reading["timestamp"]["_seconds"])
                else:
                    timestamp = datetime.utcnow()
                
                filtered_readings.append({
                    "id": reading.get("_id", str(ObjectId())),
                    "soilMoisture": reading["soilMoisture"],
                    "timestamp": timestamp,
                    "deviceId": reading.get("device_id", "esp32-2")
                })
        
        # Sort by timestamp descending and take the most recent ones
        filtered_readings.sort(key=lambda x: x["timestamp"], reverse=True)
        recent_readings = filtered_readings[:limit]
        
        # Sort by timestamp ascending for chart (oldest to newest)
        recent_readings.sort(key=lambda x: x["timestamp"])
        
        print(f"📈 Returning {len(recent_readings)} recent readings for charts")
        return recent_readings
        
    except Exception as e:
        print(f"❌ Error fetching recent soil moisture readings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching recent soil moisture readings: {str(e)}")