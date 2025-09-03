# from fastapi import APIRouter, HTTPException, Depends, Body, Request, status
# from fastapi.responses import JSONResponse
# from datetime import datetime, timedelta
# from app.services.database import get_database
# from pydantic import BaseModel
# from typing import Optional, Dict, List, Any
# from bson import ObjectId
# import json

# router = APIRouter(prefix="/api")

# # Pydantic Models
# class SensorReading(BaseModel):
#     device_id: Optional[str] = None
#     temperature: Optional[float] = None
#     humidity: Optional[float] = None
#     soilMoisture: Optional[float] = None
#     soilPh: Optional[float] = None
#     nitrogen: Optional[float] = None
#     phosphorus: Optional[float] = None
#     potassium: Optional[float] = None
#     timestamp: Optional[datetime] = None

# class WaterLevelReading(BaseModel):
#     device_id: Optional[str] = None
#     waterLevel: float
#     timestamp: Optional[datetime] = None

# class Schedule(BaseModel):
#     id: Optional[str] = None
#     mode: str  # one-time, daily, weekly
#     scheduledTime: int  # timestamp or milliseconds since midnight
#     duration: int  # minutes
#     days: Optional[Dict[str, bool]] = None
#     notifyWatering: bool = True
#     skipIfRain: bool = False
#     waterFlowRate: Optional[str] = None
#     completed: bool = False

# class ScheduleHistory(BaseModel):
#     scheduleId: str
#     mode: str
#     originalScheduledTime: int
#     actualStartTime: int
#     completedAt: int
#     duration: int
#     days: Optional[Dict[str, bool]] = None
#     dayOfWeek: Optional[int] = None
#     notifyWatering: bool
#     skipIfRain: bool
#     waterFlowRate: Optional[str] = None

# class NotificationCreate(BaseModel):
#     message: str
#     title: str
#     severity: str = "info"
#     uniqueKey: Optional[str] = None
#     contextData: Optional[Dict[str, Any]] = None
#     type: str = "system"

# class MotorControl(BaseModel):
#     status: str  # on/off
#     scheduleId: Optional[str] = None

# # Helper functions
# def convert_firestore_timestamp(timestamp_data):
#     """Convert Firestore timestamp format to datetime"""
#     if isinstance(timestamp_data, dict) and '_seconds' in timestamp_data:
#         return datetime.fromtimestamp(timestamp_data['_seconds'])
#     return timestamp_data

# def convert_to_firestore_timestamp(dt):
#     """Convert datetime to Firestore timestamp format"""
#     return {
#         "_seconds": int(dt.timestamp()),
#         "_nanoseconds": 0
#     }

# def get_philippine_time():
#     """Get current time in Philippine Time (UTC+8)"""
#     utc_now = datetime.utcnow()
#     ph_time = utc_now + timedelta(hours=8)
#     return ph_time

# def get_philippine_time_from_utc(utc_time):
#     """Convert UTC time to Philippine Time"""
#     if isinstance(utc_time, datetime):
#         return utc_time + timedelta(hours=8)
#     return utc_time

# # Sensor endpoints
# @router.get("/sensors/water-level/latest")
# async def get_latest_water_level(db=Depends(get_database)):
#     collection = db["water_level_readings"]
#     reading = await collection.find().sort("timestamp", -1).limit(1).to_list(1)
#     if not reading:
#         raise HTTPException(status_code=404, detail="No water level data found")
    
#     reading = reading[0]
#     reading['timestamp'] = convert_firestore_timestamp(reading.get('timestamp'))
#     return reading

# @router.get("/sensors/combined/latest")
# async def get_combined_sensor_data(db=Depends(get_database)):
#     try:
#         # Get latest water level
#         water_collection = db["water_level_readings"]
#         water_data = await water_collection.find().sort("timestamp", -1).limit(1).to_list(1)
        
#         # Get latest sensor readings from both ESP32 devices
#         sensor_collection = db["sensor_readings"]
#         sensor1_doc = await sensor_collection.find_one({"_id": "esp32-1"})
#         sensor2_doc = await sensor_collection.find_one({"_id": "esp32-2"})
        
#         # Get latest readings from each device
#         sensor1_latest = None
#         sensor2_latest = None
        
#         if sensor1_doc and 'readings' in sensor1_doc and sensor1_doc['readings']:
#             sensor1_latest = sensor1_doc['readings'][0]
#             sensor1_latest['timestamp'] = convert_firestore_timestamp(sensor1_latest.get('timestamp'))
        
#         if sensor2_doc and 'readings' in sensor2_doc and sensor2_doc['readings']:
#             sensor2_latest = sensor2_doc['readings'][0]
#             sensor2_latest['timestamp'] = convert_firestore_timestamp(sensor2_latest.get('timestamp'))
        
#         water_latest = water_data[0] if water_data else {}
#         water_latest['timestamp'] = convert_firestore_timestamp(water_latest.get('timestamp'))
        
#         return {
#             "waterData": water_latest,
#             "sensor1Data": sensor1_latest or {},
#             "sensor2Data": sensor2_latest or {}
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching sensor data: {str(e)}")

# @router.get("/sensors/npk-ph/latest")
# async def get_latest_npk_ph_data(db=Depends(get_database)):
#     """Get latest NPK and pH data from ESP32-1"""
#     try:
#         collection = db["sensor_readings"]
#         doc = await collection.find_one({"_id": "esp32-1"})
        
#         if not doc or 'readings' not in doc or not doc['readings']:
#             raise HTTPException(status_code=404, detail="No NPK/pH data found")
        
#         latest = doc['readings'][0]
#         latest['timestamp'] = convert_firestore_timestamp(latest.get('timestamp'))
#         return latest
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching NPK/pH data: {str(e)}")

# @router.get("/sensors/environment/latest")
# async def get_latest_environment_data(db=Depends(get_database)):
#     """Get latest temperature, humidity, soil moisture from ESP32-2"""
#     try:
#         collection = db["sensor_readings"]
#         doc = await collection.find_one({"_id": "esp32-2"})
        
#         if not doc or 'readings' not in doc or not doc['readings']:
#             raise HTTPException(status_code=404, detail="No environment data found")
        
#         latest = doc['readings'][0]
#         latest['timestamp'] = convert_firestore_timestamp(latest.get('timestamp'))
#         return latest
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching environment data: {str(e)}")

# # Schedule endpoints
# @router.get("/schedules/active")
# async def get_active_schedules(db=Depends(get_database)):
#     try:
#         collection = db["watering_schedules"]
#         schedules_root = await collection.find_one({"_id": "schedules_root"})
        
#         if not schedules_root:
#             return []
        
#         active_schedules = []
#         current_time = datetime.utcnow()
        
#         # Check all schedule types
#         for schedule_type in ["daily", "weekly", "one_time"]:
#             if schedule_type in schedules_root and schedules_root[schedule_type]:
#                 for schedule in schedules_root[schedule_type]:
#                     # Skip completed one-time schedules
#                     if schedule_type == "one_time" and schedule.get("completed"):
#                         continue
                    
#                     # Convert to standard format
#                     formatted_schedule = {
#                         "id": schedule.get("_id"),
#                         "mode": "one-time" if schedule_type == "one_time" else schedule_type,
#                         "scheduledTime": schedule.get("scheduledTime", 0),
#                         "duration": schedule.get("duration", 0),
#                         "days": schedule.get("days", {}),
#                         "notifyWatering": schedule.get("notifyWatering", True),
#                         "skipIfRain": schedule.get("skipIfRain", False),
#                         "waterFlowRate": schedule.get("waterFlowRate", "medium"),
#                         "completed": schedule.get("completed", False)
#                     }
                    
#                     active_schedules.append(formatted_schedule)
        
#         return active_schedules
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching schedules: {str(e)}")

# @router.post("/schedules/history")
# async def create_schedule_history(history_data: dict, db=Depends(get_database)):
#     try:
#         print(f"💾 Saving schedule history: {history_data}")
        
#         collection = db["watering_schedules"]
        
#         # Create history entry that matches your database structure
#         history_entry = {
#             "_id": str(ObjectId()),
#             "scheduleId": history_data.get("scheduleId"),
#             "mode": history_data.get("mode"),
#             "originalScheduledTime": history_data.get("originalScheduledTime"),
#             "actualStartTime": history_data.get("actualStartTime"),
#             "completedAt": history_data.get("completedAt"),
#             "duration": history_data.get("duration"),
#             "days": history_data.get("days", {}),
#             "dayOfWeek": history_data.get("dayOfWeek"),
#             "notifyWatering": history_data.get("notifyWatering", True),
#             "skipIfRain": history_data.get("skipIfRain", False),
#             "waterFlowRate": history_data.get("waterFlowRate", "medium"),
#             "createdAt": {
#                 "_seconds": int(datetime.utcnow().timestamp()),
#                 "_nanoseconds": 0
#             }
#         }
        
#         print(f"📝 History entry prepared: {history_entry}")
        
#         # Add to history array in schedules_root document
#         result = await collection.update_one(
#             {"_id": "schedules_root"},
#             {"$push": {"history": history_entry}}
#         )
        
#         if result.modified_count == 0:
#             # If schedules_root doesn't exist, create it with history array
#             await collection.update_one(
#                 {"_id": "schedules_root"},
#                 {
#                     "$setOnInsert": {
#                         "history": [history_entry],
#                         "daily": [],
#                         "weekly": [],
#                         "one_time": []
#                     }
#                 },
#                 upsert=True
#             )
#             print("✅ Created schedules_root document with history")
#         else:
#             print(f"✅ History saved successfully to schedules_root, modified count: {result.modified_count}")
        
#         return {"id": history_entry["_id"], "status": "success"}
        
#     except Exception as e:
#         print(f"❌ Error saving schedule history: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error saving schedule history: {str(e)}")

# @router.put("/schedules/{schedule_id}/complete")
# async def mark_schedule_completed(schedule_id: str, db=Depends(get_database)):
#     try:
#         collection = db["watering_schedules"]
        
#         # Try all schedule types
#         schedule_types = ["one_time", "daily", "weekly"]
#         updated = False
#         schedule_type = None
        
#         for s_type in schedule_types:
#             result = await collection.update_one(
#                 {"_id": "schedules_root", f"{s_type}._id": schedule_id},
#                 {"$set": {f"{s_type}.$.completed": True}}
#             )
            
#             if result.modified_count > 0:
#                 updated = True
#                 schedule_type = s_type
#                 break
        
#         if not updated:
#             # Try to find the schedule to see if it exists
#             schedules_root = await collection.find_one({"_id": "schedules_root"})
#             schedule_found = False
            
#             for s_type in schedule_types:
#                 if s_type in schedules_root:
#                     for schedule in schedules_root[s_type]:
#                         if schedule.get("_id") == schedule_id:
#                             schedule_found = True
#                             break
            
#             if not schedule_found:
#                 return JSONResponse(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     content={"error": "Schedule not found"}
#                 )
            
#             # Schedule exists but wasn't updated (maybe already completed)
#             return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content={"status": "success", "message": "Schedule may already be completed"}
#             )
        
#         print(f"✅ Schedule {schedule_id} marked as completed in {schedule_type}")
#         return {"status": "success", "schedule_type": schedule_type}
        
#     except Exception as e:
#         print(f"❌ Error marking schedule complete: {str(e)}")
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={"error": f"Error marking schedule complete: {str(e)}"}
#         )

# @router.get("/schedules/history")
# async def get_schedule_history(
#     days: Optional[int] = 7,
#     limit: Optional[int] = 50,
#     db=Depends(get_database)
# ):
#     try:
#         collection = db["watering_schedules"]
#         schedules_root = await collection.find_one({"_id": "schedules_root"})
        
#         if not schedules_root or "history" not in schedules_root:
#             return []
        
#         # Get recent history (last X days)
#         cutoff_time = datetime.utcnow() - timedelta(days=days)
#         cutoff_timestamp = int(cutoff_time.timestamp()) * 1000  # Convert to milliseconds
        
#         recent_history = [
#             history for history in schedules_root["history"]
#             if history.get("completedAt", 0) >= cutoff_timestamp
#         ]
        
#         # Sort by completedAt descending and limit results
#         recent_history.sort(key=lambda x: x.get("completedAt", 0), reverse=True)
        
#         return recent_history[:limit]
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching schedule history: {str(e)}")

# # Notification endpoints
# @router.post("/notifications")
# async def create_notification(request: Request, db=Depends(get_database)):
#     """
#     Completely flexible notification endpoint that accepts any JSON
#     without Pydantic validation
#     """
#     try:
#         # Get the raw JSON data
#         raw_data = await request.json()
#         print(f"📩 Received notification data: {raw_data}")
        
#         collection = db["notifications"]
        
#         # Extract basic fields with safe defaults
#         message = raw_data.get("message", "No message provided")
#         title = raw_data.get("title", "Notification")
#         severity = raw_data.get("severity", "info")
#         unique_key = raw_data.get("uniqueKey")
#         context_data = raw_data.get("contextData")
#         notification_type = raw_data.get("type", "system")
        
#         # Build the notification document
#         notification_dict = {
#             "_id": str(ObjectId()),
#             "message": str(message),
#             "title": str(title),
#             "severity": str(severity),
#             "type": str(notification_type),
#             "timestamp": {
#                 "_seconds": int(datetime.utcnow().timestamp()),
#                 "_nanoseconds": 0
#             },
#             "read": False,
#             "formattedDate": datetime.utcnow().strftime("%a, %B %d, %Y")
#         }
        
#         # Add optional fields if they exist
#         if unique_key is not None:
#             notification_dict["uniqueKey"] = str(unique_key)
        
#         if context_data is not None:
#             # Handle context data safely
#             if isinstance(context_data, (dict, list, str, int, float, bool)):
#                 notification_dict["contextData"] = context_data
#             else:
#                 # Convert to string if it's not a basic type
#                 notification_dict["contextData"] = str(context_data)
        
#         print(f"💾 Inserting notification: {notification_dict}")
        
#         # Insert into database
#         result = await collection.insert_one(notification_dict)
        
#         print(f"✅ Notification saved with ID: {result.inserted_id}")
        
#         return {
#             "id": str(result.inserted_id),
#             "status": "success",
#             "message": "Notification created successfully"
#         }
        
#     except json.JSONDecodeError:
#         print("❌ Invalid JSON received")
#         raise HTTPException(status_code=400, detail="Invalid JSON data")
#     except Exception as e:
#         print(f"❌ Error creating notification: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# # Add a simple test endpoint to verify the API is working
# @router.post("/notifications/test")
# async def test_notification_endpoint():
#     """Test endpoint to verify the notification API is working"""
#     return {
#         "status": "success",
#         "message": "Notification endpoint is working",
#         "timestamp": datetime.utcnow().isoformat()
#     }

# @router.get("/notifications/test-get")
# async def test_notification_get():
#     """Test GET endpoint"""
#     return {
#         "status": "success", 
#         "message": "GET endpoint is working",
#         "timestamp": datetime.utcnow().isoformat()
#     }

# @router.get("/notifications")
# async def get_notifications(
#     unread_only: Optional[bool] = True,
#     limit: Optional[int] = 50,
#     db=Depends(get_database)
# ):
#     try:
#         collection = db["notifications"]
        
#         query = {"read": False} if unread_only else {}
#         notifications = await collection.find(query).sort("timestamp", -1).limit(limit).to_list(limit)
        
#         # Convert Firestore timestamp format
#         for notification in notifications:
#             notification["id"] = str(notification["_id"])
#             notification['timestamp'] = convert_firestore_timestamp(notification.get('timestamp'))
        
#         return notifications
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

# @router.get("/notifications/unread-count")
# async def get_unread_notifications_count(db=Depends(get_database)):
#     try:
#         collection = db["notifications"]
#         count = await collection.count_documents({
#             "$or": [
#                 {"read": False},
#                 {"read": {"$exists": False}}
#             ]
#         })
#         return {"count": count, "endpoint": "notifications/unread-count"}
#     except Exception as e:
#         return {"count": 0, "error": str(e)}

# # Variation 2: Different path
# @router.get("/notifications_unread_count")
# async def get_unread_notifications_count_v2(db=Depends(get_database)):
#     try:
#         collection = db["notifications"]
#         count = await collection.count_documents({
#             "$or": [
#                 {"read": False},
#                 {"read": {"$exists": False}}
#             ]
#         })
#         return {"count": count}
#     except Exception as e:
#         return {"count": 0, "error": str(e)}

# # Variation 3: Root level endpoint
# @router.get("/unread-count")
# async def get_unread_notifications_count_v3(db=Depends(get_database)):
#     try:
#         collection = db["notifications"]
#         count = await collection.count_documents({
#             "$or": [
#                 {"read": False},
#                 {"read": {"$exists": False}}
#             ]
#         })
#         return {"count": count, "endpoint": "unread-count"}
#     except Exception as e:
#         return {"count": 0, "error": str(e)}

# @router.put("/notifications/{notification_id}/read")
# async def mark_notification_read(notification_id: str, db=Depends(get_database)):
#     try:
#         collection = db["notifications"]
#         result = await collection.update_one(
#             {"_id": notification_id},
#             {"$set": {"read": True, "readAt": datetime.utcnow()}}
#         )
        
#         if result.modified_count == 0:
#             raise HTTPException(status_code=404, detail="Notification not found")
        
#         return {"status": "success"}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error marking notification read: {str(e)}")

# @router.get("/notifications/check-today")
# async def check_notification_today(uniqueKey: str, db=Depends(get_database)):
#     try:
#         collection = db["notifications"]
        
#         # Get start of today in UTC
#         today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#         today_start_timestamp = {
#             "_seconds": int(today_start.timestamp()),
#             "_nanoseconds": 0
#         }
        
#         # Check if notification with this uniqueKey exists today
#         count = await collection.count_documents({
#             "uniqueKey": uniqueKey,
#             "timestamp._seconds": {"$gte": today_start_timestamp["_seconds"]}
#         })
        
#         return {"exists": count > 0}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error checking notification: {str(e)}")

# # Device endpoints
# @router.post("/devices/motor/control")
# async def control_motor(control: MotorControl, db=Depends(get_database)):
#     try:
#         print(f"🎛️ Motor control request: status={control.status}, scheduleId={control.scheduleId}")
        
#         collection = db["motor_status"]
#         ph_time = get_philippine_time()  # Use Philippine time
        
#         # Create motor status update for current document
#         motor_status = {
#             "status": control.status == "on",
#             "action": control.status,
#             "scheduleId": control.scheduleId,
#             "timestamp": ph_time,
#             "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p"),
#             "device_id": "main_motor",
#             "user": "system",
#             "relatedSchedule": control.scheduleId,
#             "timezone": "UTC+8",
#             "philippine_time": True
#         }
        
#         # Create history entry for motor_history document
#         history_entry = {
#             "_id": str(ObjectId()),
#             "status": control.status == "on",
#             "action": control.status,
#             "scheduleId": control.scheduleId,
#             "triggeredBy": "schedule",
#             "timestamp": ph_time,
#             "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p"),
#             "timezone": "UTC+8",
#             "philippine_time": True,
#             "type": "motor_status_update"
#         }
        
#         # Update current status document
#         current_result = await collection.update_one(
#             {"_id": "current"},
#             {"$set": motor_status},
#             upsert=True
#         )
        
#         print(f"✅ Current motor status updated: {motor_status['status']}")
        
#         # Update motor_history document with new history entry
#         history_result = await collection.update_one(
#             {"_id": "motor_history"},
#             {
#                 "$push": {
#                     "history": {
#                         "$each": [history_entry],
#                         "$slice": -200  # Keep last 200 history entries
#                     }
#                 },
#                 "$setOnInsert": {
#                     "created_at": datetime.utcnow(),
#                     "type": "motor_history"
#                 }
#             },
#             upsert=True
#         )
        
#         print(f"✅ Motor history saved to motor_history document: {history_result.modified_count} modified")
        
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "status": "success", 
#                 "action": control.status, 
#                 "motor_status": motor_status['status'],
#                 "scheduleId": control.scheduleId,
#                 "timestamp": ph_time.isoformat(),
#                 "formattedTime": motor_status['formattedTime'],
#                 "history_saved": True
#             }
#         )
        
#     except Exception as e:
#         print(f"❌ Motor control error: {str(e)}")
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={"error": f"Error controlling motor: {str(e)}"}
#         )

# @router.get("/devices/motor/history")
# async def get_motor_history(limit: int = 50, db=Depends(get_database)):
#     try:
#         collection = db["motor_status"]
#         history_doc = await collection.find_one({"_id": "motor_history"})
        
#         if not history_doc or "history" not in history_doc:
#             return []
        
#         # Get recent history, limited by the requested amount
#         history = history_doc.get("history", [])
#         recent_history = history[-limit:] if limit < len(history) else history
        
#         # Convert timestamps to ISO format if they're datetime objects
#         for item in recent_history:
#             if "timestamp" in item and isinstance(item["timestamp"], datetime):
#                 item["timestamp"] = item["timestamp"].isoformat()
        
#         return recent_history
        
#     except Exception as e:
#         print(f"❌ Error fetching motor history: {str(e)}")
#         return []

# @router.get("/devices/motor/status")
# async def get_motor_status(db=Depends(get_database)):
#     try:
#         collection = db["motor_status"]
#         status_doc = await collection.find_one({"_id": "current"})
        
#         if not status_doc:
#             # Return default status
#             return {
#                 "status": False,
#                 "action": "off",
#                 "scheduleId": None,
#                 "timestamp": get_philippine_time().isoformat(),
#                 "formattedTime": get_philippine_time().strftime("%a, %b %d, %I:%M %p"),
#                 "device_id": "main_motor",
#                 "user": "system",
#                 "philippine_time": True,
#                 "history_count": 0
#             }
        
#         # Convert timestamp to ISO format if it's a datetime object
#         if "timestamp" in status_doc and isinstance(status_doc["timestamp"], datetime):
#             status_doc["timestamp"] = status_doc["timestamp"].isoformat()
        
#         # Get history count from motor_history document
#         history_doc = await collection.find_one({"_id": "motor_history"})
#         history_count = len(history_doc["history"]) if history_doc and "history" in history_doc else 0
        
#         # Ensure consistent response format
#         response = {
#             "status": status_doc.get("status", False),
#             "action": status_doc.get("action", "off"),
#             "scheduleId": status_doc.get("scheduleId"),
#             "timestamp": status_doc.get("timestamp"),
#             "formattedTime": status_doc.get("formattedTime"),
#             "device_id": status_doc.get("device_id", "main_motor"),
#             "user": status_doc.get("user", "system"),
#             "philippine_time": status_doc.get("philippine_time", True),
#             "history_count": history_count
#         }
        
#         return response
        
#     except Exception as e:
#         print(f"❌ Error fetching motor status: {str(e)}")
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "status": False,
#                 "action": "off",
#                 "error": str(e),
#                 "timestamp": get_philippine_time().isoformat(),
#                 "philippine_time": True
#             }
#         )

# # Add this to your notification endpoints in the router
# @router.get("/notifications/check-today")
# async def check_notification_today(uniqueKey: str, db=Depends(get_database)):
#     try:
#         collection = db["notifications"]
        
#         # Get start of today in UTC
#         today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#         today_start_timestamp = convert_to_firestore_timestamp(today_start)
        
#         # Check if notification with this uniqueKey exists today
#         count = await collection.count_documents({
#             "uniqueKey": uniqueKey,
#             "timestamp._seconds": {"$gte": today_start_timestamp["_seconds"]}
#         })
        
#         return {"exists": count > 0}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error checking notification: {str(e)}")
    
# @router.get("/notifications/check-today")
# async def check_notification_today(uniqueKey: str, db=Depends(get_database)):
#     try:
#         collection = db["notifications"]
        
#         # Get start of today in UTC
#         today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#         today_start_timestamp = convert_to_firestore_timestamp(today_start)
        
#         # Check if notification with this uniqueKey exists today
#         count = await collection.count_documents({
#             "uniqueKey": uniqueKey,
#             "timestamp._seconds": {"$gte": today_start_timestamp["_seconds"]}
#         })
        
#         return {"exists": count > 0}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error checking notification: {str(e)}")

# # Health check endpoint
# @router.get("/health")
# async def health_check(db=Depends(get_database)):
#     try:
#         # Test database connection
#         await db.command("ping")
#         return {"status": "healthy", "database": "connected"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

from fastapi import APIRouter, HTTPException, Depends, Body, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from app.services.database import get_database
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from bson import ObjectId
import json

router = APIRouter(prefix="/api")

# Pydantic Models
class SensorReading(BaseModel):
    device_id: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    soilMoisture: Optional[float] = None
    soilPh: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    timestamp: Optional[datetime] = None

class WaterLevelReading(BaseModel):
    device_id: Optional[str] = None
    waterLevel: float
    timestamp: Optional[datetime] = None

class Schedule(BaseModel):
    id: Optional[str] = None
    mode: str  # one-time, daily, weekly
    scheduledTime: int  # timestamp or milliseconds since midnight
    duration: int  # minutes
    days: Optional[Dict[str, bool]] = None
    notifyWatering: bool = True
    skipIfRain: bool = False
    waterFlowRate: Optional[str] = None
    completed: bool = False

class ScheduleHistory(BaseModel):
    scheduleId: str
    mode: str
    originalScheduledTime: int
    actualStartTime: int
    completedAt: int
    duration: int
    days: Optional[Dict[str, bool]] = None
    dayOfWeek: Optional[int] = None
    notifyWatering: bool
    skipIfRain: bool
    waterFlowRate: Optional[str] = None

class NotificationCreate(BaseModel):
    message: str
    title: str
    severity: str = "info"
    uniqueKey: Optional[str] = None
    contextData: Optional[Dict[str, Any]] = None
    type: str = "system"

class MotorControl(BaseModel):
    status: str  # on/off
    scheduleId: Optional[str] = None

# Helper functions
def convert_firestore_timestamp(timestamp_data):
    """Convert Firestore timestamp format to datetime"""
    if isinstance(timestamp_data, dict) and '_seconds' in timestamp_data:
        return datetime.fromtimestamp(timestamp_data['_seconds'])
    return timestamp_data

def convert_to_firestore_timestamp(dt):
    """Convert datetime to Firestore timestamp format"""
    return {
        "_seconds": int(dt.timestamp()),
        "_nanoseconds": 0
    }

def get_philippine_time():
    """Get current time in Philippine Time (UTC+8)"""
    utc_now = datetime.utcnow()
    ph_time = utc_now + timedelta(hours=8)
    return ph_time

def get_philippine_time_from_utc(utc_time):
    """Convert UTC time to Philippine Time"""
    if isinstance(utc_time, datetime):
        return utc_time + timedelta(hours=8)
    return utc_time

# Sensor endpoints
@router.get("/sensors/water-level/latest")
async def get_latest_water_level(db=Depends(get_database)):
    collection = db["water_level_readings"]
    reading = await collection.find().sort("timestamp", -1).limit(1).to_list(1)
    if not reading:
        raise HTTPException(status_code=404, detail="No water level data found")
    
    reading = reading[0]
    reading['timestamp'] = convert_firestore_timestamp(reading.get('timestamp'))
    return reading

@router.get("/sensors/combined/latest")
async def get_combined_sensor_data(db=Depends(get_database)):
    try:
        # Get latest water level
        water_collection = db["water_level_readings"]
        water_data = await water_collection.find().sort("timestamp", -1).limit(1).to_list(1)
        
        # Get latest sensor readings from both ESP32 devices
        sensor_collection = db["sensor_readings"]
        sensor1_doc = await sensor_collection.find_one({"_id": "esp32-1"})
        sensor2_doc = await sensor_collection.find_one({"_id": "esp32-2"})
        
        # Get latest readings from each device
        sensor1_latest = None
        sensor2_latest = None
        
        if sensor1_doc and 'readings' in sensor1_doc and sensor1_doc['readings']:
            sensor1_latest = sensor1_doc['readings'][0]
            sensor1_latest['timestamp'] = convert_firestore_timestamp(sensor1_latest.get('timestamp'))
        
        if sensor2_doc and 'readings' in sensor2_doc and sensor2_doc['readings']:
            sensor2_latest = sensor2_doc['readings'][0]
            sensor2_latest['timestamp'] = convert_firestore_timestamp(sensor2_latest.get('timestamp'))
        
        water_latest = water_data[0] if water_data else {}
        water_latest['timestamp'] = convert_firestore_timestamp(water_latest.get('timestamp'))
        
        return {
            "waterData": water_latest,
            "sensor1Data": sensor1_latest or {},
            "sensor2Data": sensor2_latest or {}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor data: {str(e)}")

@router.get("/sensors/npk-ph/latest")
async def get_latest_npk_ph_data(db=Depends(get_database)):
    """Get latest NPK and pH data from ESP32-1"""
    try:
        collection = db["sensor_readings"]
        doc = await collection.find_one({"_id": "esp32-1"})
        
        if not doc or 'readings' not in doc or not doc['readings']:
            raise HTTPException(status_code=404, detail="No NPK/pH data found")
        
        latest = doc['readings'][0]
        latest['timestamp'] = convert_firestore_timestamp(latest.get('timestamp'))
        return latest
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching NPK/pH data: {str(e)}")

@router.get("/sensors/environment/latest")
async def get_latest_environment_data(db=Depends(get_database)):
    """Get latest temperature, humidity, soil moisture from ESP32-2"""
    try:
        collection = db["sensor_readings"]
        doc = await collection.find_one({"_id": "esp32-2"})
        
        if not doc or 'readings' not in doc or not doc['readings']:
            raise HTTPException(status_code=404, detail="No environment data found")
        
        latest = doc['readings'][0]
        latest['timestamp'] = convert_firestore_timestamp(latest.get('timestamp'))
        return latest
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching environment data: {str(e)}")

# Schedule endpoints
@router.get("/schedules/active")
async def get_active_schedules(db=Depends(get_database)):
    try:
        collection = db["watering_schedules"]
        schedules_root = await collection.find_one({"_id": "schedules_root"})
        
        if not schedules_root:
            return []
        
        active_schedules = []
        current_time = datetime.utcnow()
        
        # Check all schedule types
        for schedule_type in ["daily", "weekly", "one_time"]:
            if schedule_type in schedules_root and schedules_root[schedule_type]:
                for schedule in schedules_root[schedule_type]:
                    # Skip completed one-time schedules
                    if schedule_type == "one_time" and schedule.get("completed"):
                        continue
                    
                    # Convert to standard format
                    formatted_schedule = {
                        "id": schedule.get("_id"),
                        "mode": "one-time" if schedule_type == "one_time" else schedule_type,
                        "scheduledTime": schedule.get("scheduledTime", 0),
                        "duration": schedule.get("duration", 0),
                        "days": schedule.get("days", {}),
                        "notifyWatering": schedule.get("notifyWatering", True),
                        "skipIfRain": schedule.get("skipIfRain", False),
                        "waterFlowRate": schedule.get("waterFlowRate", "medium"),
                        "completed": schedule.get("completed", False)
                    }
                    
                    active_schedules.append(formatted_schedule)
        
        return active_schedules
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching schedules: {str(e)}")

@router.post("/schedules/history")
async def create_schedule_history(history_data: dict, db=Depends(get_database)):
    try:
        print(f"💾 Saving schedule history: {history_data}")
        
        collection = db["watering_schedules"]
        
        # Create history entry that matches your database structure
        history_entry = {
            "_id": str(ObjectId()),
            "scheduleId": history_data.get("scheduleId"),
            "mode": history_data.get("mode"),
            "originalScheduledTime": history_data.get("originalScheduledTime"),
            "actualStartTime": history_data.get("actualStartTime"),
            "completedAt": history_data.get("completedAt"),
            "duration": history_data.get("duration"),
            "days": history_data.get("days", {}),
            "dayOfWeek": history_data.get("dayOfWeek"),
            "notifyWatering": history_data.get("notifyWatering", True),
            "skipIfRain": history_data.get("skipIfRain", False),
            "waterFlowRate": history_data.get("waterFlowRate", "medium"),
            "createdAt": {
                "_seconds": int(datetime.utcnow().timestamp()),
                "_nanoseconds": 0
            }
        }
        
        print(f"📝 History entry prepared: {history_entry}")
        
        # Add to history array in schedules_root document
        result = await collection.update_one(
            {"_id": "schedules_root"},
            {"$push": {"history": history_entry}}
        )
        
        if result.modified_count == 0:
            # If schedules_root doesn't exist, create it with history array
            await collection.update_one(
                {"_id": "schedules_root"},
                {
                    "$setOnInsert": {
                        "history": [history_entry],
                        "daily": [],
                        "weekly": [],
                        "one_time": []
                    }
                },
                upsert=True
            )
            print("✅ Created schedules_root document with history")
        else:
            print(f"✅ History saved successfully to schedules_root, modified count: {result.modified_count}")
        
        return {"id": history_entry["_id"], "status": "success"}
        
    except Exception as e:
        print(f"❌ Error saving schedule history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving schedule history: {str(e)}")

@router.put("/schedules/{schedule_id}/complete")
async def mark_schedule_completed(schedule_id: str, db=Depends(get_database)):
    try:
        collection = db["watering_schedules"]
        
        # Try all schedule types
        schedule_types = ["one_time", "daily", "weekly"]
        updated = False
        schedule_type = None
        
        for s_type in schedule_types:
            result = await collection.update_one(
                {"_id": "schedules_root", f"{s_type}._id": schedule_id},
                {"$set": {f"{s_type}.$.completed": True}}
            )
            
            if result.modified_count > 0:
                updated = True
                schedule_type = s_type
                break
        
        if not updated:
            # Try to find the schedule to see if it exists
            schedules_root = await collection.find_one({"_id": "schedules_root"})
            schedule_found = False
            
            for s_type in schedule_types:
                if s_type in schedules_root:
                    for schedule in schedules_root[s_type]:
                        if schedule.get("_id") == schedule_id:
                            schedule_found = True
                            break
            
            if not schedule_found:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"error": "Schedule not found"}
                )
            
            # Schedule exists but wasn't updated (maybe already completed)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "success", "message": "Schedule may already be completed"}
            )
        
        print(f"✅ Schedule {schedule_id} marked as completed in {schedule_type}")
        return {"status": "success", "schedule_type": schedule_type}
        
    except Exception as e:
        print(f"❌ Error marking schedule complete: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Error marking schedule complete: {str(e)}"}
        )

@router.get("/schedules/history")
async def get_schedule_history(
    days: Optional[int] = 7,
    limit: Optional[int] = 50,
    db=Depends(get_database)
):
    try:
        collection = db["watering_schedules"]
        schedules_root = await collection.find_one({"_id": "schedules_root"})
        
        if not schedules_root or "history" not in schedules_root:
            return []
        
        # Get recent history (last X days)
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        cutoff_timestamp = int(cutoff_time.timestamp()) * 1000  # Convert to milliseconds
        
        recent_history = [
            history for history in schedules_root["history"]
            if history.get("completedAt", 0) >= cutoff_timestamp
        ]
        
        # Sort by completedAt descending and limit results
        recent_history.sort(key=lambda x: x.get("completedAt", 0), reverse=True)
        
        return recent_history[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching schedule history: {str(e)}")

# Notification endpoints - UPDATED
# @router.post("/notifications")
# async def create_notification(request: Request, db=Depends(get_database)):
#     """
#     Completely flexible notification endpoint that accepts any JSON
#     without Pydantic validation
#     """
#     try:
#         # Get the raw JSON data
#         raw_data = await request.json()
#         print(f"📩 Received notification data: {raw_data}")
        
#         collection = db["notifications"]
        
#         # Extract basic fields with safe defaults
#         message = raw_data.get("message", "No message provided")
#         title = raw_data.get("title", "Notification")
#         severity = raw_data.get("severity", "info")
#         unique_key = raw_data.get("uniqueKey")
#         context_data = raw_data.get("contextData", {})  # Default to empty dict
#         notification_type = raw_data.get("type", "system")
        
#         # Build the notification document
#         notification_dict = {
#             "_id": str(ObjectId()),
#             "message": str(message),
#             "title": str(title),
#             "severity": str(severity),
#             "type": str(notification_type),
#             "timestamp": {
#                 "_seconds": int(datetime.utcnow().timestamp()),
#                 "_nanoseconds": 0
#             },
#             "read": False,
#             "formattedDate": datetime.utcnow().strftime("%a, %B %d, %Y"),
#             "contextData": context_data  # Always include contextData
#         }
        
#         # Add optional fields if they exist
#         if unique_key is not None:
#             notification_dict["uniqueKey"] = str(unique_key)
        
#         print(f"💾 Inserting notification with context: {json.dumps(notification_dict, indent=2)}")
        
#         # Insert into database
#         result = await collection.insert_one(notification_dict)
        
#         print(f"✅ Notification saved with ID: {result.inserted_id}")
        
#         return {
#             "id": str(result.inserted_id),
#             "status": "success",
#             "message": "Notification created successfully"
#         }
        
#     except json.JSONDecodeError:
#         print("❌ Invalid JSON received")
#         raise HTTPException(status_code=400, detail="Invalid JSON data")
#     except Exception as e:
#         print(f"❌ Error creating notification: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/notifications")
async def create_notification(request: Request, db=Depends(get_database)):
    """
    Enhanced notification endpoint with better error handling and validation
    """
    try:
        # Get the raw JSON data
        raw_data = await request.json()
        print(f"📩 Raw notification data received: {json.dumps(raw_data, indent=2, default=str)}")
        
        collection = db["notifications"]
        
        # Validate required fields
        if not raw_data.get("message"):
            raise HTTPException(status_code=400, detail="Message field is required")
        
        if not raw_data.get("title"):
            raise HTTPException(status_code=400, detail="Title field is required")
        
        # Extract and validate basic fields
        message = str(raw_data.get("message", "")).strip()
        title = str(raw_data.get("title", "")).strip()
        severity = str(raw_data.get("severity", "info")).lower()
        unique_key = raw_data.get("uniqueKey")
        notification_type = str(raw_data.get("type", "system"))
        
        # Validate severity
        valid_severities = ["info", "warning", "error", "critical", "success"]
        if severity not in valid_severities:
            severity = "info"
        
        # Handle context data properly - accept both context and contextData
        context_data = raw_data.get("contextData") or raw_data.get("context") or {}
        
        # Clean and validate context data
        def clean_context_data(data):
            """Recursively clean context data to ensure MongoDB compatibility"""
            if data is None:
                return {}
            if isinstance(data, (str, int, float, bool)):
                return data
            if isinstance(data, list):
                return [clean_context_data(item) for item in data][:50]  # Limit array size
            if isinstance(data, dict):
                cleaned = {}
                for key, value in data.items():
                    # Ensure key is a valid string
                    clean_key = str(key).strip()
                    if clean_key and not clean_key.startswith('$'):  # Avoid MongoDB operator keys
                        try:
                            # Limit depth of nested objects
                            if isinstance(value, dict) and len(cleaned) < 20:  # Limit object properties
                                cleaned[clean_key] = clean_context_data(value)
                            elif not isinstance(value, dict):
                                cleaned[clean_key] = clean_context_data(value)
                        except Exception as e:
                            print(f"Warning: Skipping problematic key '{clean_key}': {e}")
                            continue
                return cleaned
            # For any other type, convert to string
            return str(data)[:500]  # Limit string length
        
        # Clean the context data
        try:
            cleaned_context = clean_context_data(context_data)
        except Exception as e:
            print(f"Warning: Error cleaning context data: {e}")
            cleaned_context = {"raw_data": str(context_data)[:500]}  # Fallback
        
        # Add metadata to context
        cleaned_context.update({
            "processed_at": datetime.utcnow().isoformat(),
            "server_timezone": "UTC",
            "data_version": "1.0"
        })
        
        # Build the notification document
        notification_dict = {
            "_id": str(ObjectId()),
            "message": message,
            "title": title,
            "severity": severity,
            "type": notification_type,
            "timestamp": {
                "_seconds": int(datetime.utcnow().timestamp()),
                "_nanoseconds": 0
            },
            "read": False,
            "formattedDate": datetime.utcnow().strftime("%a, %B %d, %Y"),
            "context": cleaned_context
        }
        
        # Add unique key if provided
        if unique_key:
            notification_dict["uniqueKey"] = str(unique_key).strip()
        
        print(f"💾 Final notification document: {json.dumps(notification_dict, indent=2, default=str)}")
        
        # Insert into database with error handling
        try:
            result = await collection.insert_one(notification_dict)
            print(f"✅ Notification saved with ID: {result.inserted_id}")
            
            return {
                "id": str(result.inserted_id),
                "status": "success",
                "message": "Notification created successfully"
            }
            
        except Exception as db_error:
            print(f"❌ Database insertion error: {str(db_error)}")
            # Try without context data if insertion fails
            notification_dict_no_context = notification_dict.copy()
            notification_dict_no_context["context"] = {"error": "Context data removed due to serialization issues"}
            
            result = await collection.insert_one(notification_dict_no_context)
            print(f"✅ Notification saved without context data: {result.inserted_id}")
            
            return {
                "id": str(result.inserted_id),
                "status": "success",
                "message": "Notification created without context data due to serialization issues"
            }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except json.JSONDecodeError as json_error:
        print(f"❌ JSON decode error: {json_error}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid JSON data: {str(json_error)}"
        )
    except Exception as e:
        print(f"❌ Unexpected error creating notification: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

# Add a debug endpoint to test notification creation
@router.post("/notifications/debug")
async def debug_notification(request: Request):
    """Debug endpoint to see exactly what data is being received"""
    try:
        raw_data = await request.json()
        return {
            "status": "debug",
            "received_data": raw_data,
            "data_type": str(type(raw_data)),
            "keys": list(raw_data.keys()) if isinstance(raw_data, dict) else "Not a dict",
            "message_present": "message" in raw_data if isinstance(raw_data, dict) else False,
            "title_present": "title" in raw_data if isinstance(raw_data, dict) else False,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": str(type(e))
        }

@router.get("/notifications/test-get")
async def test_notification_get():
    """Test GET endpoint"""
    return {
        "status": "success", 
        "message": "GET endpoint is working",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/notifications")
async def get_notifications(
    unread_only: Optional[bool] = True,
    limit: Optional[int] = 50,
    db=Depends(get_database)
):
    try:
        collection = db["notifications"]
        
        query = {"read": False} if unread_only else {}
        notifications = await collection.find(query).sort("timestamp", -1).limit(limit).to_list(limit)
        
        # Convert Firestore timestamp format
        for notification in notifications:
            notification["id"] = str(notification["_id"])
            notification['timestamp'] = convert_firestore_timestamp(notification.get('timestamp'))
        
        return notifications
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

@router.get("/notifications/unread-count")
async def get_unread_notifications_count(db=Depends(get_database)):
    try:
        collection = db["notifications"]
        count = await collection.count_documents({
            "$or": [
                {"read": False},
                {"read": {"$exists": False}}
            ]
        })
        return {"count": count, "endpoint": "notifications/unread-count"}
    except Exception as e:
        return {"count": 0, "error": str(e)}

# Variation 2: Different path
@router.get("/notifications_unread_count")
async def get_unread_notifications_count_v2(db=Depends(get_database)):
    try:
        collection = db["notifications"]
        count = await collection.count_documents({
            "$or": [
                {"read": False},
                {"read": {"$exists": False}}
            ]
        })
        return {"count": count}
    except Exception as e:
        return {"count": 0, "error": str(e)}

# Variation 3: Root level endpoint
@router.get("/unread-count")
async def get_unread_notifications_count_v3(db=Depends(get_database)):
    try:
        collection = db["notifications"]
        count = await collection.count_documents({
            "$or": [
                {"read": False},
                {"read": {"$exists": False}}
            ]
        })
        return {"count": count, "endpoint": "unread-count"}
    except Exception as e:
        return {"count": 0, "error": str(e)}

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, db=Depends(get_database)):
    try:
        collection = db["notifications"]
        result = await collection.update_one(
            {"_id": notification_id},
            {"$set": {"read": True, "readAt": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {"status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking notification read: {str(e)}")

@router.get("/notifications/check-today")
async def check_notification_today(uniqueKey: str, db=Depends(get_database)):
    try:
        collection = db["notifications"]
        
        # Get start of today in UTC
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_start_timestamp = convert_to_firestore_timestamp(today_start)
        
        # Check if notification with this uniqueKey exists today
        count = await collection.count_documents({
            "uniqueKey": uniqueKey,
            "timestamp._seconds": {"$gte": today_start_timestamp["_seconds"]}
        })
        
        return {"exists": count > 0}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking notification: {str(e)}")

# Device endpoints
@router.post("/devices/motor/control")
async def control_motor(control: MotorControl, db=Depends(get_database)):
    try:
        print(f"🎛️ Motor control request: status={control.status}, scheduleId={control.scheduleId}")
        
        collection = db["motor_status"]
        ph_time = get_philippine_time()  # Use Philippine time
        
        # Create motor status update for current document
        motor_status = {
            "status": control.status == "on",
            "action": control.status,
            "scheduleId": control.scheduleId,
            "timestamp": ph_time,
            "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p"),
            "device_id": "main_motor",
            "user": "system",
            "relatedSchedule": control.scheduleId,
            "timezone": "UTC+8",
            "philippine_time": True
        }
        
        # Create history entry for motor_history document
        history_entry = {
            "_id": str(ObjectId()),
            "status": control.status == "on",
            "action": control.status,
            "scheduleId": control.scheduleId,
            "triggeredBy": "schedule",
            "timestamp": ph_time,
            "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p"),
            "timezone": "UTC+8",
            "philippine_time": True,
            "type": "motor_status_update"
        }
        
        # Update current status document
        current_result = await collection.update_one(
            {"_id": "current"},
            {"$set": motor_status},
            upsert=True
        )
        
        print(f"✅ Current motor status updated: {motor_status['status']}")
        
        # Update motor_history document with new history entry
        history_result = await collection.update_one(
            {"_id": "motor_history"},
            {
                "$push": {
                    "history": {
                        "$each": [history_entry],
                        "$slice": -200  # Keep last 200 history entries
                    }
                },
                "$setOnInsert": {
                    "created_at": datetime.utcnow(),
                    "type": "motor_history"
                }
            },
            upsert=True
        )
        
        print(f"✅ Motor history saved to motor_history document: {history_result.modified_count} modified")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success", 
                "action": control.status, 
                "motor_status": motor_status['status'],
                "scheduleId": control.scheduleId,
                "timestamp": ph_time.isoformat(),
                "formattedTime": motor_status['formattedTime'],
                "history_saved": True
            }
        )
        
    except Exception as e:
        print(f"❌ Motor control error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Error controlling motor: {str(e)}"}
        )

@router.get("/devices/motor/history")
async def get_motor_history(limit: int = 50, db=Depends(get_database)):
    try:
        collection = db["motor_status"]
        history_doc = await collection.find_one({"_id": "motor_history"})
        
        if not history_doc or "history" not in history_doc:
            return []
        
        # Get recent history, limited by the requested amount
        history = history_doc.get("history", [])
        recent_history = history[-limit:] if limit < len(history) else history
        
        # Convert timestamps to ISO format if they're datetime objects
        for item in recent_history:
            if "timestamp" in item and isinstance(item["timestamp"], datetime):
                item["timestamp"] = item["timestamp"].isoformat()
        
        return recent_history
        
    except Exception as e:
        print(f"❌ Error fetching motor history: {str(e)}")
        return []

@router.get("/devices/motor/status")
async def get_motor_status(db=Depends(get_database)):
    try:
        collection = db["motor_status"]
        status_doc = await collection.find_one({"_id": "current"})
        
        if not status_doc:
            # Return default status
            return {
                "status": False,
                "action": "off",
                "scheduleId": None,
                "timestamp": get_philippine_time().isoformat(),
                "formattedTime": get_philippine_time().strftime("%a, %b %d, %I:%M %p"),
                "device_id": "main_motor",
                "user": "system",
                "philippine_time": True,
                "history_count": 0
            }
        
        # Convert timestamp to ISO format if it's a datetime object
        if "timestamp" in status_doc and isinstance(status_doc["timestamp"], datetime):
            status_doc["timestamp"] = status_doc["timestamp"].isoformat()
        
        # Get history count from motor_history document
        history_doc = await collection.find_one({"_id": "motor_history"})
        history_count = len(history_doc["history"]) if history_doc and "history" in history_doc else 0
        
        # Ensure consistent response format
        response = {
            "status": status_doc.get("status", False),
            "action": status_doc.get("action", "off"),
            "scheduleId": status_doc.get("scheduleId"),
            "timestamp": status_doc.get("timestamp"),
            "formattedTime": status_doc.get("formattedTime"),
            "device_id": status_doc.get("device_id", "main_motor"),
            "user": status_doc.get("user", "system"),
            "philippine_time": status_doc.get("philippine_time", True),
            "history_count": history_count
        }
        
        return response
        
    except Exception as e:
        print(f"❌ Error fetching motor status: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": False,
                "action": "off",
                "error": str(e),
                "timestamp": get_philippine_time().isoformat(),
                "philippine_time": True
            }
        )

# Health check endpoint
@router.get("/health")
async def health_check(db=Depends(get_database)):
    try:
        # Test database connection
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")