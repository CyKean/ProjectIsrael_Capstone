# app/routers/watering_schedules.py
from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime, timedelta
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from app.services.database import get_database

router = APIRouter(prefix="/api", tags=["watering"])

# ==================== MODELS ====================
class WateringScheduleResponse(BaseModel):
    id: str
    mode: str
    duration: int
    days: Optional[List[bool]] = None
    skipIfRain: bool = False
    notifyWatering: bool = True
    waterFlowRate: str = "medium"
    scheduledTime: Optional[int] = None
    dateTime: Optional[str] = None
    completed: bool = False
    createdAt: str
    updatedAt: str

class MotorStatusResponse(BaseModel):
    status: bool
    device_id: str
    formattedTime: Optional[str] = None
    timestamp: str  # This should be string, not datetime

class ScheduleHistoryResponse(BaseModel):
    id: str
    scheduleId: str
    mode: str
    duration: int
    completedAt: str  # This should be string, not datetime
    days: Optional[List[bool]] = None
    dayOfWeek: Optional[int] = None
    notifyWatering: bool
    skipIfRain: bool
    waterFlowRate: str

class SoilMoistureResponse(BaseModel):
    moisture: float
    timestamp: str  # This should be string, not datetime
    device_id: str

# ==================== ROUTES ====================
@router.get("/watering-schedules", response_model=List[WateringScheduleResponse])
async def get_watering_schedules():
    """Get all watering schedules from all subcollections"""
    try:
        db = await get_database()
        collection = db["watering_schedules"]
        root_doc = await collection.find_one({"_id": "schedules_root"})
        
        if not root_doc:
            return []
        
        result = []
        
        # Process daily schedules
        daily_schedules = root_doc.get("daily", [])
        if isinstance(daily_schedules, list):
            for schedule in daily_schedules:
                if isinstance(schedule, dict):
                    result.append(process_schedule(schedule, "daily"))
        
        # Process weekly schedules
        weekly_schedules = root_doc.get("weekly", [])
        if isinstance(weekly_schedules, list):
            for schedule in weekly_schedules:
                if isinstance(schedule, dict):
                    result.append(process_schedule(schedule, "weekly"))
        
        # Process one-time schedules
        one_time_schedules = root_doc.get("one_time", [])
        if isinstance(one_time_schedules, list):
            for schedule in one_time_schedules:
                if isinstance(schedule, dict):
                    result.append(process_schedule(schedule, "one-time"))
        
        return result
    except Exception as e:
        print(f"Error in get_watering_schedules: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching schedules: {str(e)}")

def ensure_string_timestamp(timestamp):
    """Convert any timestamp format to string"""
    if timestamp is None:
        return ""
    
    if isinstance(timestamp, str):
        return timestamp
    
    if isinstance(timestamp, datetime):
        return timestamp.isoformat()
    
    if isinstance(timestamp, dict):
        # Handle Firebase timestamp format {_seconds: X, _nanoseconds: Y}
        if "_seconds" in timestamp:
            seconds = timestamp.get("_seconds", 0)
            nanoseconds = timestamp.get("_nanoseconds", 0)
            dt = datetime.fromtimestamp(seconds + nanoseconds / 1e9)
            return dt.isoformat()
    
    # Fallback: convert to string
    return str(timestamp)

@router.post("/motor-status-ph")
async def set_motor_status_philippine_time(status: dict):
    """Set motor status with Philippine Time (UTC+8) and save to separate history document"""
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        new_status = status.get("status", False)
        source = status.get("source", "manual")
        
        # Get current Philippine Time (UTC+8)
        utc_now = datetime.utcnow()
        ph_time = utc_now + timedelta(hours=8)
        
        # Create history item with Philippine Time (as string)
        history_item = {
            "_id": str(ObjectId()),
            "status": new_status,
            "device_id": "main_motor",
            "source": source,
            "timestamp": ph_time.isoformat() + "+08:00",  # String format
            "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p"),
            "philippine_time": True
        }
        
        # Update current status (as string)
        update_data = {
            "status": new_status,
            "device_id": "main_motor",
            "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p"),
            "timestamp": ph_time.isoformat() + "+08:00",  # String format
            "philippine_time": True
        }
        
        # Update the current status document
        await collection.update_one(
            {"_id": "current"},
            {"$set": update_data},
            upsert=True
        )
        
        # Add to history document - create it if it doesn't exist
        await collection.update_one(
            {"_id": "motor_history"},
            {
                "$setOnInsert": {  # Only set these fields on insert (creation)
                    "created_at": datetime.utcnow(),
                    "type": "motor_history"
                },
                "$push": {
                    "history": {
                        "$each": [history_item],
                        "$slice": -1000  # Keep last 1000 items
                    }
                }
            },
            upsert=True  # This creates the document if it doesn't exist
        )
        
        if not new_status:
            await cancel_ongoing_watering_schedules(db, source)
        
        return {
            "message": "Motor status updated successfully",
            "timestamp": ph_time.isoformat() + "+08:00",  # String format
            "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p")
        }
        
    except Exception as e:
        print(f"Error in set_motor_status_philippine_time: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error setting motor status: {str(e)}")

@router.post("/initialize-motor-history")
async def initialize_motor_history():
    """Initialize the motor history document if it doesn't exist"""
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Check if history document exists
        history_doc = await collection.find_one({"_id": "motor_history"})
        
        if not history_doc:
            # Create empty history document
            await collection.insert_one({
                "_id": "motor_history",
                "history": [],
                "created_at": datetime.utcnow(),
                "type": "motor_history"
            })
            return {"message": "Motor history document created successfully"}
        else:
            return {"message": "Motor history document already exists"}
            
    except Exception as e:
        print(f"Error in initialize_motor_history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error initializing motor history: {str(e)}")

@router.get("/motor-status-ph", response_model=MotorStatusResponse)
async def get_motor_status_philippine_time():
    """Get current motor status with Philippine Time"""
    try:
        db = await get_database()
        collection = db["motor_status"]
        status = await collection.find_one({"_id": "current"})
        
        if not status:
            ph_time = datetime.utcnow() + timedelta(hours=8)
            return {
                "status": False,
                "device_id": "main_motor",
                "formattedTime": ph_time.strftime("%a, %b %d, %I:%M %p"),
                "timestamp": ph_time.isoformat() + "+08:00"
            }
        
        # Use the utility function to ensure timestamp is string
        timestamp = ensure_string_timestamp(status.get("timestamp"))
        
        return {
            "status": status.get("status", False),
            "device_id": status.get("device_id", "main_motor"),
            "formattedTime": status.get("formattedTime"),
            "timestamp": timestamp
        }
    except Exception as e:
        print(f"Error in get_motor_status_philippine_time: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching motor status: {str(e)}")

@router.get("/motor-history-ph", response_model=List[MotorStatusResponse])
async def get_motor_history_philippine_time(
    limit: int = Query(20, description="Number of history entries to return")
):
    """Get motor status history from separate history document"""
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the history document - handle case where it doesn't exist
        history_doc = await collection.find_one({"_id": "motor_history"})
        
        # If document doesn't exist, return empty array
        if not history_doc:
            return []
        
        # Extract the history array from the document - handle case where history doesn't exist
        history_data = history_doc.get("history", [])
        if not isinstance(history_data, list):
            return []
        
        result = []
        for item in history_data:
            if isinstance(item, dict):
                # Use the utility function to ensure timestamp is string
                timestamp = ensure_string_timestamp(item.get("timestamp"))
                
                result.append({
                    "status": item.get("status", False),
                    "device_id": item.get("device_id", "main_motor"),
                    "formattedTime": item.get("formattedTime"),
                    "timestamp": timestamp,
                    "source": item.get("source", "manual")
                })
        
        # Return most recent items first
        return list(reversed(result))[:limit]
        
    except Exception as e:
        print(f"Error in get_motor_history_philippine_time: {str(e)}")
        # Return empty array instead of crashing
        return []
    
@router.get("/motor-status", response_model=MotorStatusResponse)
async def get_motor_status():
    """Get current motor status"""
    try:
        db = await get_database()
        collection = db["motor_status"]
        status = await collection.find_one({"_id": "current"})
        
        if not status:
            return {
                "status": False,
                "device_id": "main_motor",
                "formattedTime": datetime.utcnow().strftime("%a, %b %d, %I:%M %p"),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Handle timestamp conversion safely
        timestamp = convert_timestamp_safe(status.get("timestamp"))
        
        # Get formatted time from status or generate it
        formatted_time = status.get("formattedTime")
        if not formatted_time:
            formatted_time = timestamp.strftime("%a, %b %d, %I:%M %p")
        
        return {
            "status": status.get("status", False),
            "device_id": status.get("device_id", "main_motor"),
            "formattedTime": formatted_time,
            "timestamp": timestamp.isoformat()
        }
    except Exception as e:
        print(f"Error in get_motor_status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching motor status: {str(e)}")

@router.get("/motor-history", response_model=List[MotorStatusResponse])
async def get_motor_history(
    limit: int = Query(20, description="Number of history entries to return")
):
    """Get motor status history"""
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the current status document which contains the history array
        current_doc = await collection.find_one({"_id": "current"})
        
        if not current_doc:
            return []
        
        # Extract the history array from the document
        history_data = current_doc.get("history", [])
        if not isinstance(history_data, list):
            return []
        
        result = []
        for item in history_data[:limit]:
            if isinstance(item, dict):
                # Convert timestamp safely - handle both object and string formats
                timestamp_data = item.get("timestamp")
                
                # Handle different timestamp formats in history items
                if isinstance(timestamp_data, dict):
                    # Firebase format with _seconds and _nanoseconds
                    seconds = timestamp_data.get("_seconds", 0)
                    nanoseconds = timestamp_data.get("_nanoseconds", 0)
                    timestamp = datetime.fromtimestamp(seconds + nanoseconds / 1e9)
                elif isinstance(timestamp_data, (int, float)):
                    # Handle both seconds and milliseconds
                    if timestamp_data > 1000000000000:  # Likely milliseconds
                        timestamp = datetime.fromtimestamp(timestamp_data / 1000)
                    else:  # Likely seconds
                        timestamp = datetime.fromtimestamp(timestamp_data)
                elif isinstance(timestamp_data, str):
                    # ISO format string
                    timestamp = datetime.fromisoformat(timestamp_data.replace('Z', '+00:00'))
                else:
                    # Fallback to current time
                    timestamp = datetime.utcnow()
                
                # Get formatted time from item or generate it
                formatted_time = item.get("formattedTime")
                if not formatted_time:
                    formatted_time = timestamp.strftime("%a, %b %d, %I:%M %p")
                
                result.append({
                    "status": item.get("status", False),
                    "device_id": item.get("device_id", "main_motor"),
                    "formattedTime": formatted_time,
                    "timestamp": timestamp.isoformat()
                })
        
        # Sort by timestamp descending (most recent first)
        result.sort(key=lambda x: x["timestamp"], reverse=True)
        return result
        
    except Exception as e:
        print(f"Error in get_motor_history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching motor history: {str(e)}")

@router.get("/schedule-history", response_model=List[ScheduleHistoryResponse])
async def get_schedule_history(db=Depends(get_database)):
    """Get schedule execution history"""
    try:
        collection = db["watering_schedules"]
        root_doc = await collection.find_one({"_id": "schedules_root"})
        
        if not root_doc:
            return []
        
        history_data = root_doc.get("history", [])
        if not isinstance(history_data, list):
            return []
        
        result = []
        for item in history_data:
            if isinstance(item, dict):
                # Convert completedAt timestamp safely
                completed_at = convert_timestamp_safe(item.get("completedAt"))
                
                # Handle days array conversion properly
                days = item.get("days", [])
                if days and isinstance(days, list):
                    # Convert any numbers to booleans (1 -> true, 0 -> false)
                    days = [bool(day) if isinstance(day, (int, float)) else day for day in days]
                    # Ensure all items are actually booleans
                    days = [bool(day) for day in days]
                else:
                    days = []
                
                result.append({
                    "id": item.get("_id", ""),
                    "scheduleId": item.get("scheduleId", ""),
                    "mode": item.get("mode", ""),
                    "duration": item.get("duration", 0),
                    "completedAt": completed_at.isoformat(),
                    "days": days,  # Use the cleaned days array
                    "dayOfWeek": item.get("dayOfWeek"),
                    "notifyWatering": bool(item.get("notifyWatering", True)),
                    "skipIfRain": bool(item.get("skipIfRain", False)),
                    "waterFlowRate": item.get("waterFlowRate", "medium")
                })
        
        # Sort by completion time descending (most recent first)
        result.sort(key=lambda x: x["completedAt"], reverse=True)
        return result
    except Exception as e:
        print(f"Error in get_schedule_history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching schedule history: {str(e)}")

@router.get("/soil-moisture", response_model=SoilMoistureResponse)
async def get_soil_moisture():
    """Get latest soil moisture reading from sensor_readings collection"""
    try:
        db = await get_database()
        collection = db["sensor_readings"]
        
        # Find the document with device_id "esp32-2"
        device_doc = await collection.find_one({"_id": "esp32-2"})
        
        if not device_doc:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Get the readings array
        readings = device_doc.get("readings", [])
        if not readings:
            raise HTTPException(status_code=404, detail="No readings available")
        
        # Find the most recent reading with soilMoisture data
        latest_reading = None
        for reading in reversed(readings):
            if "soilMoisture" in reading:
                latest_reading = reading
                break
        
        if not latest_reading:
            raise HTTPException(status_code=404, detail="No soil moisture readings available")
        
        # Convert Firebase timestamp to ISO format
        timestamp_data = latest_reading.get("timestamp", {})
        if isinstance(timestamp_data, dict) and "_seconds" in timestamp_data:
            seconds = timestamp_data.get("_seconds", 0)
            nanoseconds = timestamp_data.get("_nanoseconds", 0)
            timestamp_dt = datetime.fromtimestamp(seconds + nanoseconds / 1e9)
            timestamp_iso = timestamp_dt.isoformat()
        else:
            timestamp_iso = datetime.utcnow().isoformat()
        
        return {
            "moisture": float(latest_reading.get("soilMoisture", 0.0)),
            "timestamp": timestamp_iso,
            "device_id": latest_reading.get("device_id", "esp32-2")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_soil_moisture: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching soil moisture: {str(e)}")


@router.put("/watering-schedules/{schedule_id}")
async def update_schedule(schedule_id: str, schedule: dict):
    """Update an existing watering schedule"""
    try:
        db = await get_database()
        collection = db["watering_schedules"]
        
        # Find the schedule in all subcollections
        root_doc = await collection.find_one({"_id": "schedules_root"})
        if not root_doc:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        # Find which subcollection contains the schedule
        subcollections = ["daily", "weekly", "one_time"]
        found_subcollection = None
        found_index = -1
        
        for subcollection in subcollections:
            schedules = root_doc.get(subcollection, [])
            for idx, s in enumerate(schedules):
                if s.get("_id") == schedule_id:
                    found_subcollection = subcollection
                    found_index = idx
                    break
            if found_subcollection:
                break
        
        if not found_subcollection or found_index == -1:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        # Check for duplicate schedules (excluding the current one being edited)
        if await check_duplicate_schedule(schedule, schedule_id, db):
            raise HTTPException(status_code=400, detail="A conflicting schedule already exists at this time")
        
        # Update the schedule
        update_data = {
            "duration": schedule.get("duration", 0),
            "days": schedule.get("days", []),
            "skipIfRain": schedule.get("skipIfRain", False),
            "notifyWatering": schedule.get("notifyWatering", True),
            "waterFlowRate": schedule.get("waterFlowRate", "medium"),
            "scheduledTime": schedule.get("scheduledTime"),
            "dateTime": schedule.get("dateTime"),
            "updatedAt": {
                "_seconds": int(datetime.utcnow().timestamp()),
                "_nanoseconds": 0
            }
        }
        
        # Update the specific schedule in the subcollection
        update_query = {
            f"{found_subcollection}.{found_index}.{key}": value 
            for key, value in update_data.items()
        }
        
        await collection.update_one(
            {"_id": "schedules_root"},
            {"$set": update_query}
        )
        
        return {"message": "Schedule updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating schedule: {str(e)}")

@router.delete("/watering-schedules/{schedule_id}")
async def delete_schedule(schedule_id: str):
    """Delete a watering schedule"""
    try:
        db = await get_database()
        collection = db["watering_schedules"]
        
        # Find which subcollection contains the schedule
        root_doc = await collection.find_one({"_id": "schedules_root"})
        if not root_doc:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        subcollections = ["daily", "weekly", "one_time"]
        found_subcollection = None
        
        for subcollection in subcollections:
            schedules = root_doc.get(subcollection, [])
            for s in schedules:
                if s.get("_id") == schedule_id:
                    found_subcollection = subcollection
                    break
            if found_subcollection:
                break
        
        if not found_subcollection:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        # Remove the schedule from the subcollection
        await collection.update_one(
            {"_id": "schedules_root"},
            {"$pull": {found_subcollection: {"_id": schedule_id}}}
        )
        
        return {"message": "Schedule deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting schedule: {str(e)}")

@router.post("/motor-status")
async def set_motor_status(status: dict):
    """Set motor status and handle watering schedule implications"""
    try:
        db = await get_database()
        motor_collection = db["motor_status"]
        schedules_collection = db["watering_schedules"]
        
        new_status = status.get("status", False)
        source = status.get("source", "manual")
        
        # Update current status
        update_data = {
            "status": new_status,
            "device_id": "main_motor",
            "formattedTime": datetime.utcnow().strftime("%a, %b %d, %I:%M %p"),
            "timestamp": {
                "_seconds": int(datetime.utcnow().timestamp()),
                "_nanoseconds": 0
            }
        }
        
        # Add to history
        history_item = {
            "_id": str(ObjectId()),
            **update_data,
            "source": source
        }
        
        # Update the motor status document
        await motor_collection.update_one(
            {"_id": "current"},
            {
                "$set": update_data,
                "$push": {"history": {"$each": [history_item], "$slice": -100}}
            },
            upsert=True
        )
        
        # If turning OFF the motor, check if we need to cancel any ongoing watering schedules
        if not new_status:
            await cancel_ongoing_watering_schedules(db, source)
        
        return {"message": "Motor status updated successfully"}
    except Exception as e:
        print(f"Error in set_motor_status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error setting motor status: {str(e)}")

async def cancel_ongoing_watering_schedules(db, cancellation_reason):
    """Cancel any ongoing watering schedules when motor is turned off"""
    try:
        collection = db["watering_schedules"]
        root_doc = await collection.find_one({"_id": "schedules_root"})
        
        if not root_doc:
            return
        
        now = datetime.utcnow()
        now_timestamp = now.timestamp() * 1000  # Convert to milliseconds
        
        # Check all subcollections for ongoing schedules
        subcollections = ["daily", "weekly", "one_time"]
        cancelled_count = 0
        
        for subcollection in subcollections:
            schedules = root_doc.get(subcollection, [])
            updates_needed = []
            
            for schedule in schedules:
                if schedule.get("completed", False):
                    continue
                
                schedule_id = schedule.get("_id")
                scheduled_time = schedule.get("scheduledTime", 0)
                duration = schedule.get("duration", 0)
                
                # Calculate schedule end time (scheduled time + duration in milliseconds)
                end_time = scheduled_time + (duration * 60 * 1000)
                
                # Check if schedule is currently ongoing (now is between start and end time)
                if scheduled_time <= now_timestamp <= end_time:
                    # Mark as completed with cancellation reason
                    updates_needed.append({
                        "schedule_id": schedule_id,
                        "update": {
                            "completed": True,
                            "cancellationReason": f"Cancelled due to manual motor turn off ({cancellation_reason})",
                            "updatedAt": {
                                "_seconds": int(now.timestamp()),
                                "_nanoseconds": 0
                            }
                        }
                    })
                    cancelled_count += 1
            
            # Apply updates to this subcollection
            for update in updates_needed:
                # Find the index of the schedule to update
                schedule_index = None
                for idx, s in enumerate(schedules):
                    if s.get("_id") == update["schedule_id"]:
                        schedule_index = idx
                        break
                
                if schedule_index is not None:
                    # Update the specific schedule
                    for key, value in update["update"].items():
                        await collection.update_one(
                            {"_id": "schedules_root"},
                            {"$set": {f"{subcollection}.{schedule_index}.{key}": value}}
                        )
        
        if cancelled_count > 0:
            print(f"Cancelled {cancelled_count} ongoing watering schedule(s) due to motor turn off")
            
    except Exception as e:
        print(f"Error in cancel_ongoing_watering_schedules: {str(e)}")

@router.post("/watering-schedules")
async def create_schedule(schedule: dict):
    """Create a new watering schedule"""
    try:
        db = await get_database()
        collection = db["watering_schedules"]
        
        # Check for duplicate schedules
        duplicate_check = await check_duplicate_schedule(schedule, None, db)
        if duplicate_check:
            raise HTTPException(status_code=400, detail="A conflicting schedule already exists at this time")
        
        # Determine which subcollection to add to based on mode
        mode = schedule.get("mode", "weekly")
        subcollection = "weekly"
        if mode == "daily":
            subcollection = "daily"
        elif mode == "one-time":
            subcollection = "one_time"
        
        # Format dateTime for display
        dateTime = ""
        scheduled_time = schedule.get("scheduledTime")
        
        if mode == "one-time" and scheduled_time:
            try:
                # Handle both milliseconds and seconds timestamps
                if scheduled_time > 1000000000000:  # Likely milliseconds
                    schedule_date = datetime.fromtimestamp(scheduled_time / 1000)
                else:  # Likely seconds
                    schedule_date = datetime.fromtimestamp(scheduled_time)
                dateTime = schedule_date.strftime("%a, %b %d, %I:%M %p")
            except Exception as e:
                print(f"Error parsing scheduled time: {e}")
                dateTime = "Invalid time"
        elif mode in ["daily", "weekly"]:
            hour = schedule.get("hour", 0)
            minute = schedule.get("minute", 0)
            display_hour = hour % 12
            if display_hour == 0:
                display_hour = 12
            am_pm = "AM" if hour < 12 else "PM"
            dateTime = f"{display_hour:02d}:{minute:02d} {am_pm}"
        
        # For one-time schedules, ensure scheduledTime is stored correctly
        if mode == "one-time" and scheduled_time:
            # Convert to milliseconds if it's in seconds
            if scheduled_time < 1000000000000:  # Likely seconds
                scheduled_time = scheduled_time * 1000
        
        # Create schedule data with Firebase timestamp format
        schedule_data = {
            "_id": str(ObjectId()),
            "duration": schedule.get("duration", 0),
            "days": schedule.get("days", []),
            "skipIfRain": schedule.get("skipIfRain", False),
            "notifyWatering": schedule.get("notifyWatering", True),
            "waterFlowRate": schedule.get("waterFlowRate", "medium"),
            "scheduledTime": scheduled_time,
            "dateTime": dateTime,
            "completed": False,
            "createdAt": {
                "_seconds": int(datetime.utcnow().timestamp()),
                "_nanoseconds": 0
            },
            "updatedAt": {
                "_seconds": int(datetime.utcnow().timestamp()),
                "_nanoseconds": 0
            }
        }
        
        # Add to the appropriate subcollection
        await collection.update_one(
            {"_id": "schedules_root"},
            {"$push": {subcollection: schedule_data}},
            upsert=True
        )
        
        return {"id": schedule_data["_id"], "message": "Schedule created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating schedule: {str(e)}")

# Enhanced duplicate checking function
async def check_duplicate_schedule(new_schedule, exclude_schedule_id, db):
    """Check if a schedule with conflicting time already exists"""
    try:
        collection = db["watering_schedules"]
        root_doc = await collection.find_one({"_id": "schedules_root"})
        
        if not root_doc:
            return False
        
        new_mode = new_schedule.get("mode", "weekly")
        new_duration = new_schedule.get("duration", 0)
        new_scheduled_time = new_schedule.get("scheduledTime")
        new_days = new_schedule.get("days", [])
        
        # Convert one-time scheduled time to milliseconds if needed
        if new_mode == "one-time" and new_scheduled_time:
            if new_scheduled_time < 1000000000000:  # Likely seconds
                new_scheduled_time = new_scheduled_time * 1000
        
        # Check all subcollections for conflicts
        subcollections = ["daily", "weekly", "one_time"]
        
        for subcollection in subcollections:
            schedules = root_doc.get(subcollection, [])
            for schedule in schedules:
                # Skip the schedule being edited
                if exclude_schedule_id and schedule.get("_id") == exclude_schedule_id:
                    continue
                
                # Skip completed schedules
                if schedule.get("completed", False):
                    continue
                
                existing_mode = "daily" if subcollection == "daily" else "weekly" if subcollection == "weekly" else "one-time"
                existing_duration = schedule.get("duration", 0)
                existing_scheduled_time = schedule.get("scheduledTime")
                existing_days = schedule.get("days", [])
                
                # Check if schedules overlap based on mode
                if await schedules_overlap(
                    new_mode, new_scheduled_time, new_duration, new_days,
                    existing_mode, existing_scheduled_time, existing_duration, existing_days
                ):
                    return True
        
        return False
    except Exception as e:
        print(f"Error in check_duplicate_schedule: {str(e)}")
        return False

# Enhanced schedules_overlap function
async def schedules_overlap(new_mode, new_time, new_duration, new_days, 
                           existing_mode, existing_time, existing_duration, existing_days):
    """Check if two schedules overlap in time"""
    try:
        # Handle None values
        if new_time is None or existing_time is None:
            return False
        
        # Convert durations to milliseconds
        new_duration_ms = new_duration * 60 * 1000
        existing_duration_ms = existing_duration * 60 * 1000
        
        # Calculate start and end times
        if new_mode == "one-time" and existing_mode == "one-time":
            # Both are one-time schedules
            new_start = new_time
            new_end = new_time + new_duration_ms
            existing_start = existing_time
            existing_end = existing_time + existing_duration_ms
            
            return max(new_start, existing_start) < min(new_end, existing_end)
        
        elif new_mode in ["daily", "weekly"] and existing_mode in ["daily", "weekly"]:
            # Both are recurring schedules - check if they have overlapping times
            new_start_ms = new_time
            new_end_ms = new_time + new_duration_ms
            existing_start_ms = existing_time
            existing_end_ms = existing_time + existing_duration_ms
            
            # Check if time ranges overlap (within the same day)
            time_overlap = max(new_start_ms, existing_start_ms) < min(new_end_ms, existing_end_ms)
            
            if not time_overlap:
                return False
            
            # For weekly schedules, check if days overlap
            if new_mode == "weekly" and existing_mode == "weekly":
                return any(nd and ed for nd, ed in zip(new_days, existing_days))
            else:
                # Daily schedules or mixed daily/weekly - always overlap if times overlap
                return True
        
        elif new_mode == "one-time" and existing_mode in ["daily", "weekly"]:
            # One-time schedule vs recurring schedule
            # Check if the one-time schedule falls on a day when the recurring schedule runs
            one_time_date = datetime.fromtimestamp(new_time / 1000)
            
            if existing_mode == "daily":
                # Daily schedule runs every day, so check time overlap
                new_start_ms = new_time % (24 * 60 * 60 * 1000)  # Time of day in ms
                new_end_ms = new_start_ms + new_duration_ms
                existing_start_ms = existing_time
                existing_end_ms = existing_time + existing_duration_ms
                
                return max(new_start_ms, existing_start_ms) < min(new_end_ms, existing_end_ms)
                
            elif existing_mode == "weekly":
                # Check if the one-time schedule falls on a scheduled day
                day_of_week = (one_time_date.weekday() + 1) % 7  # Convert to 0=Sunday, 6=Saturday
                if existing_days[day_of_week]:
                    # Check time overlap
                    new_start_ms = new_time % (24 * 60 * 60 * 1000)  # Time of day in ms
                    new_end_ms = new_start_ms + new_duration_ms
                    existing_start_ms = existing_time
                    existing_end_ms = existing_time + existing_duration_ms
                    
                    return max(new_start_ms, existing_start_ms) < min(new_end_ms, existing_end_ms)
            
        elif existing_mode == "one-time" and new_mode in ["daily", "weekly"]:
            # Recurring schedule vs one-time schedule (reverse of above)
            one_time_date = datetime.fromtimestamp(existing_time / 1000)
            
            if new_mode == "daily":
                # Daily schedule runs every day, so check time overlap
                existing_start_ms = existing_time % (24 * 60 * 60 * 1000)  # Time of day in ms
                existing_end_ms = existing_start_ms + existing_duration_ms
                new_start_ms = new_time
                new_end_ms = new_time + new_duration_ms
                
                return max(new_start_ms, existing_start_ms) < min(new_end_ms, existing_end_ms)
                
            elif new_mode == "weekly":
                # Check if the one-time schedule falls on a scheduled day
                day_of_week = (one_time_date.weekday() + 1) % 7  # Convert to 0=Sunday, 6=Saturday
                if new_days[day_of_week]:
                    # Check time overlap
                    existing_start_ms = existing_time % (24 * 60 * 60 * 1000)  # Time of day in ms
                    existing_end_ms = existing_start_ms + existing_duration_ms
                    new_start_ms = new_time
                    new_end_ms = new_time + new_duration_ms
                    
                    return max(new_start_ms, existing_start_ms) < min(new_end_ms, existing_end_ms)
        
        return False
            
    except Exception as e:
        print(f"Error in schedules_overlap: {str(e)}")
        return False

def process_schedule(schedule, mode):
    """Process a schedule document from MongoDB"""
    # Convert timestamps safely
    created_at = convert_timestamp_safe(schedule.get("createdAt"))
    updated_at = convert_timestamp_safe(schedule.get("updatedAt"))
    
    # Handle days array conversion
    days = schedule.get("days", [])
    if days and isinstance(days, list):
        days = [bool(day) if isinstance(day, (int, float)) else day for day in days]
        days = [bool(day) for day in days]
    else:
        days = []
    
    return {
        "id": schedule.get("_id", ""),
        "mode": mode,
        "duration": schedule.get("duration", 0),
        "days": days,
        "skipIfRain": schedule.get("skipIfRain", False),
        "notifyWatering": schedule.get("notifyWatering", True),
        "waterFlowRate": schedule.get("waterFlowRate", "medium"),
        "scheduledTime": schedule.get("scheduledTime"),
        "dateTime": schedule.get("dateTime"),
        "completed": schedule.get("completed", False),
        "createdAt": created_at.isoformat(),
        "updatedAt": updated_at.isoformat()
    }

# FIXED: Enhanced timestamp conversion function
def convert_timestamp_safe(timestamp_data):
    """Convert timestamp safely, handling various formats"""
    try:
        if timestamp_data is None:
            return datetime.utcnow()
            
        if isinstance(timestamp_data, dict):
            # Firebase timestamp format with _seconds and _nanoseconds
            seconds = timestamp_data.get("_seconds", 0)
            nanoseconds = timestamp_data.get("_nanoseconds", 0)
            return datetime.fromtimestamp(seconds + nanoseconds / 1e9)
        elif isinstance(timestamp_data, (int, float)):
            # Handle both seconds and milliseconds
            if timestamp_data > 1000000000000:  # Likely milliseconds
                return datetime.fromtimestamp(timestamp_data / 1000)
            else:  # Likely seconds
                return datetime.fromtimestamp(timestamp_data)
        elif isinstance(timestamp_data, str):
            # ISO format string
            return datetime.fromisoformat(timestamp_data.replace('Z', '+00:00'))
        else:
            return datetime.utcnow()
    except Exception as e:
        print(f"Error converting timestamp {timestamp_data}: {str(e)}")
        return datetime.utcnow()