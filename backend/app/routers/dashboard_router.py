# routers/sensor_router.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.services.database import get_database

router = APIRouter(prefix="/api", tags=["sensors"])

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def serialize_document(doc):
    """Convert MongoDB document to JSON serializable format"""
    if not doc:
        return None
    doc = doc.copy()
    doc['_id'] = str(doc['_id'])
    return doc

def convert_firestore_timestamp(timestamp_dict):
    """Convert Firestore timestamp format to datetime"""
    if isinstance(timestamp_dict, dict) and '_seconds' in timestamp_dict:
        return datetime.fromtimestamp(timestamp_dict['_seconds'] + timestamp_dict.get('_nanoseconds', 0) / 1e9)
    return datetime.now()

# @router.get("/stream")
# async def stream_sensor_data(db = Depends(get_database)):
#     """Server-Sent Events stream for real-time sensor data"""
#     async def event_generator():
#         try:
#             sensor_readings = db["sensor_readings"]
#             water_level_readings = db["water_level_readings"]
            
#             devices = ["esp32-1", "esp32-2", "esp32-3"]
            
#             # Send initial data for all devices
#             for device in devices:
#                 if device == "esp32-3":
#                     # Water level device - flat structure
#                     latest_data = await water_level_readings.find_one(
#                         {"deviceId": device},
#                         sort=[("timestamp", -1)]
#                     )
#                 else:
#                     # Sensor device - get latest reading from readings array
#                     device_doc = await sensor_readings.find_one({"_id": device})
#                     if device_doc and device_doc.get("readings"):
#                         latest_data = device_doc["readings"][-1] if device_doc["readings"] else None
#                     else:
#                         latest_data = None
                
#                 if latest_data:
#                     event_data = {
#                         "type": device,
#                         "data": {
#                             "nitrogen": latest_data.get("nitrogen", 0),
#                             "phosphorus": latest_data.get("phosphorus", 0),
#                             "potassium": latest_data.get("potassium", 0),
#                             "soilPh": latest_data.get("soilPh", 7.0),
#                             "temperature": latest_data.get("temperature", 0),
#                             "humidity": latest_data.get("humidity", 0),
#                             "soilMoisture": latest_data.get("soilMoisture", 0),
#                             "waterLevel": latest_data.get("waterLevel", 0)
#                         }
#                     }
                    
#                     yield f"data: {json.dumps(event_data, cls=JSONEncoder)}\n\n"
#                     await asyncio.sleep(0.1)
            
#             # Keep connection alive and check for new data periodically
#             while True:
#                 await asyncio.sleep(5)
                
#                 for device in devices:
#                     if device == "esp32-3":
#                         latest_data = await water_level_readings.find_one(
#                             {"deviceId": device},
#                             sort=[("timestamp", -1)]
#                         )
#                     else:
#                         device_doc = await sensor_readings.find_one({"_id": device})
#                         if device_doc and device_doc.get("readings"):
#                             latest_data = device_doc["readings"][-1] if device_doc["readings"] else None
#                         else:
#                             latest_data = None
                    
#                     if latest_data:
#                         event_data = {
#                             "type": device,
#                             "data": {
#                                 "nitrogen": latest_data.get("nitrogen", 0),
#                                 "phosphorus": latest_data.get("phosphorus", 0),
#                                 "potassium": latest_data.get("potassium", 0),
#                                 "soilPh": latest_data.get("soilPh", 7.0),
#                                 "temperature": latest_data.get("temperature", 0),
#                                 "humidity": latest_data.get("humidity", 0),
#                                 "soilMoisture": latest_data.get("soilMoisture", 0),
#                                 "waterLevel": latest_data.get("waterLevel", 0)
#                             }
#                         }
                        
#                         yield f"data: {json.dumps(event_data, cls=JSONEncoder)}\n\n"
        
#         except Exception as e:
#             yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
#     return StreamingResponse(
#         event_generator(),
#         media_type="text/event-stream",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#             "Access-Control-Allow-Origin": "*"
#         }
#     )

@router.get("/sensor-data/latest")
async def get_latest_sensor_data(db = Depends(get_database)):
    """Get latest sensor data from all devices"""
    try:
        sensor_readings = db["sensor_readings"]
        water_level_readings = db["water_level_readings"]
        
        devices = ["esp32-1", "esp32-2", "esp32-3"]
        result = {}
        
        for device in devices:
            if device == "esp32-3":
                # Water level device - flat structure
                data = await water_level_readings.find_one(
                    {"deviceId": device},
                    sort=[("timestamp", -1)]
                )
                if data:
                    result[device] = serialize_document(data)
            else:
                # Sensor device - get latest reading from readings array
                device_doc = await sensor_readings.find_one({"_id": device})
                if device_doc and device_doc.get("readings") and device_doc["readings"]:
                    latest_reading = device_doc["readings"][-1]
                    result[device] = serialize_document(latest_reading)
        
        return result
    
    except Exception as e:
        print(f"Error in get_latest_sensor_data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/sensor-data/all")
async def get_all_sensor_data(db = Depends(get_database)):
    """Get all sensor data organized by device type"""
    try:
        sensor_readings = db["sensor_readings"]
        water_level_readings = db["water_level_readings"]
        
        result = {
            "npkData": [],      # esp32-1: Nitrogen, Phosphorus, Potassium, Soil pH
            "envData": [],      # esp32-2: Temperature, Humidity, Soil Moisture
            "waterData": []     # esp32-3: Water Level
        }
        
        # Get ESP32-1 data (NPK and pH) - get the 50 most recent readings
        device_doc = await sensor_readings.find_one({"_id": "esp32-1"})
        if device_doc and device_doc.get("readings"):
            # Get the most recent readings (limit to 50)
            recent_readings = device_doc["readings"][-50:] if len(device_doc["readings"]) > 50 else device_doc["readings"]
            
            for reading in recent_readings:
                reading_timestamp = reading.get("timestamp")
                if isinstance(reading_timestamp, dict) and '_seconds' in reading_timestamp:
                    reading_timestamp = convert_firestore_timestamp(reading_timestamp)
                
                result["npkData"].append({
                    "nitrogen": float(reading.get("nitrogen", 0)),
                    "phosphorus": float(reading.get("phosphorus", 0)),
                    "potassium": float(reading.get("potassium", 0)),
                    "soilPh": float(reading.get("soilPh", 7.0)),
                    "timestamp": reading_timestamp or datetime.now()
                })
        
        # Get ESP32-2 data (Environmental) - get the 50 most recent readings
        device_doc = await sensor_readings.find_one({"_id": "esp32-2"})
        if device_doc and device_doc.get("readings"):
            # Get the most recent readings (limit to 50)
            recent_readings = device_doc["readings"][-50:] if len(device_doc["readings"]) > 50 else device_doc["readings"]
            
            for reading in recent_readings:
                reading_timestamp = reading.get("timestamp")
                if isinstance(reading_timestamp, dict) and '_seconds' in reading_timestamp:
                    reading_timestamp = convert_firestore_timestamp(reading_timestamp)
                
                result["envData"].append({
                    "temperature": float(reading.get("temperature", 0)),
                    "humidity": float(reading.get("humidity", 0)),
                    "soilMoisture": float(reading.get("soilMoisture", 0)),
                    "timestamp": reading_timestamp or datetime.now()
                })
        
        # Get ESP32-3 data (Water Level) - get the 50 most recent readings
        cursor = water_level_readings.find({"deviceId": "esp32-3"}).sort("timestamp", -1).limit(50)
        water_data = await cursor.to_list(length=50)
        for item in water_data:
            if item:
                result["waterData"].append({
                    "waterLevel": float(item.get("waterLevel", 0)),
                    "timestamp": item.get("timestamp", datetime.now())
                })
        
        # Ensure all timestamps are datetime objects and sort by timestamp
        for data_type in result:
            for item in result[data_type]:
                if isinstance(item.get("timestamp"), str):
                    try:
                        item["timestamp"] = datetime.fromisoformat(item["timestamp"].replace('Z', '+00:00'))
                    except:
                        item["timestamp"] = datetime.now()
            
            # Sort by timestamp (oldest first)
            result[data_type].sort(key=lambda x: x.get("timestamp", datetime.now()))
        
        return result
    
    except Exception as e:
        print(f"Error in get_all_sensor_data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/water-level/latest")
async def get_latest_water_level(db = Depends(get_database)):
    """Get latest water level reading"""
    try:
        water_level_readings = db["water_level_readings"]
        
        data = await water_level_readings.find_one(
            sort=[("timestamp", -1)]
        )
        
        if data:
            return serialize_document(data)
        
        # Return default if no data found
        return {"waterLevel": 0, "timestamp": datetime.now().isoformat(), "deviceId": "esp32-3"}
    
    except Exception as e:
        print(f"Error in get_latest_water_level: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/motor-status/current")
async def get_current_motor_status(db = Depends(get_database)):
    """Get current motor status"""
    try:
        motor_status = db["motor_status"]
        
        # Motor status is stored with _id: "current"
        data = await motor_status.find_one({"_id": "current"})
        
        if data:
            return serialize_document(data)
        
        # Return default if no data found
        return {"status": False, "timestamp": datetime.now().isoformat(), "type": "current"}
    
    except Exception as e:
        print(f"Error in get_current_motor_status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/motor-status/history")
async def get_motor_history(
    week_only: bool = True,
    db = Depends(get_database)
):
    """Get motor status history"""
    try:
        motor_status = db["motor_status"]
        
        # Get the current status document which contains history array
        current_status = await motor_status.find_one({"_id": "current"})
        
        if not current_status or not current_status.get("history"):
            return []
        
        history_data = current_status["history"]
        
        if week_only:
            start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
            # Filter history by timestamp
            filtered_history = []
            for item in history_data:
                item_timestamp = item.get("timestamp")
                # Handle Firestore timestamp format
                if isinstance(item_timestamp, dict) and '_seconds' in item_timestamp:
                    item_timestamp = convert_firestore_timestamp(item_timestamp)
                
                if item_timestamp and item_timestamp >= start_of_week:
                    filtered_history.append(item)
            history_data = filtered_history
        
        # Serialize and ensure proper format
        serialized_data = [serialize_document(item) for item in history_data if item]
        
        # Ensure all documents have required fields
        for item in serialized_data:
            item.setdefault('status', False)
            item.setdefault('timestamp', datetime.now().isoformat())
            item.setdefault('type', 'status_update')
        
        return serialized_data
    
    except Exception as e:
        print(f"Error in get_motor_history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/sensor-data")
async def create_sensor_reading(
    reading: Dict[str, Any],
    db = Depends(get_database)
):
    """Create a new sensor reading"""
    try:
        sensor_readings = db["sensor_readings"]
        water_level_readings = db["water_level_readings"]
        
        # Add timestamp if not provided
        if "timestamp" not in reading:
            reading["timestamp"] = datetime.now()
        
        # Ensure deviceId is present
        device_id = reading.get("deviceId")
        if not device_id:
            raise HTTPException(status_code=400, detail="deviceId is required")
        
        # Insert into appropriate collection based on device type
        if device_id == "esp32-3":
            water_reading = {
                "waterLevel": reading.get("waterLevel", 0),
                "timestamp": reading["timestamp"],
                "deviceId": "esp32-3"
            }
            result = await water_level_readings.insert_one(water_reading)
        else:
            # For sensor devices, add to the readings array
            device_doc = await sensor_readings.find_one({"_id": device_id})
            if device_doc:
                # Update existing device document
                await sensor_readings.update_one(
                    {"_id": device_id},
                    {"$push": {"readings": reading}}
                )
            else:
                # Create new device document
                new_device = {
                    "_id": device_id,
                    "readings": [reading]
                }
                result = await sensor_readings.insert_one(new_device)
        
        return {"message": "Reading created successfully"}
    
    except Exception as e:
        print(f"Error in create_sensor_reading: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/motor-status")
async def update_motor_status(
    status_data: Dict[str, Any],
    db = Depends(get_database)
):
    """Update motor status and add to history"""
    try:
        motor_status = db["motor_status"]
        
        timestamp = datetime.now()
        status = status_data.get("status", False)
        
        # Update current status and add to history
        await motor_status.update_one(
            {"_id": "current"},
            {
                "$set": {
                    "status": status,
                    "timestamp": timestamp,
                    "device_id": "main_motor",
                    "user": "system"
                },
                "$push": {
                    "history": {
                        "status": status,
                        "timestamp": timestamp,
                        "triggeredBy": status_data.get("triggeredBy", "manual")
                    }
                }
            },
            upsert=True
        )
        
        return {"message": "Motor status updated successfully"}
    
    except Exception as e:
        print(f"Error in update_motor_status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health")
async def health_check(db = Depends(get_database)):
    """Health check endpoint"""
    try:
        # Test database connection
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/debug/collections")
async def debug_collections(db = Depends(get_database)):
    """Debug endpoint to check collections and documents"""
    try:
        collections = await db.list_collection_names()
        result = {}
        
        for collection_name in collections:
            collection = db[collection_name]
            count = await collection.count_documents({})
            cursor = collection.find().limit(2)
            sample = await cursor.to_list(length=2)
            result[collection_name] = {
                "count": count,
                "sample": [serialize_document(doc) for doc in sample]
            }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")