from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from bson import ObjectId
import json

from app.services.database import get_database

router = APIRouter(prefix="/api")

# JSON encoder to handle ObjectId serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

def convert_timestamp(timestamp_data):
    """Convert various timestamp formats to timezone-aware datetime"""
    if isinstance(timestamp_data, datetime):
        # If it's already a datetime, ensure it's timezone-aware
        if timestamp_data.tzinfo is None:
            return timestamp_data.replace(tzinfo=timezone.utc)
        return timestamp_data
    elif isinstance(timestamp_data, dict) and '_seconds' in timestamp_data:
        # Firebase timestamp format: {_seconds: 123456789, _nanoseconds: 0}
        return datetime.fromtimestamp(timestamp_data['_seconds'], tz=timezone.utc)
    elif isinstance(timestamp_data, str):
        # ISO string format
        try:
            # Handle both "2025-09-04T08:14:41.509+00:00" and "2025-09-04T08:14:41.509Z"
            if timestamp_data.endswith('Z'):
                timestamp_data = timestamp_data[:-1] + '+00:00'
            
            # Parse as timezone-aware datetime
            dt = datetime.fromisoformat(timestamp_data)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            return datetime.now(timezone.utc)
    else:
        return datetime.now(timezone.utc)

def make_timezone_aware(dt):
    """Ensure datetime is timezone-aware"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

@router.get("/motor-control/history")
async def get_motor_control_history(
    limit: int = Query(1000, ge=1, le=5000),
    skip: int = Query(0, ge=0)
):
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the motor history document
        history_doc = await collection.find_one({"_id": "motor_history"})
        
        if not history_doc:
            # Fallback: try to find any document with history array
            history_doc = await collection.find_one({"history": {"$exists": True}})
            if not history_doc:
                # Return empty array instead of error for frontend compatibility
                return []
        
        # Extract and format history data
        history_data = history_doc.get("history", [])
        
        if not history_data:
            return []
        
        # Sort history by timestamp (newest first)
        def get_sort_key(item):
            timestamp = item.get("timestamp")
            converted = convert_timestamp(timestamp)
            return make_timezone_aware(converted)
        
        history_data.sort(key=get_sort_key, reverse=True)
        
        # Apply pagination
        paginated_data = history_data[skip:skip + limit]
        
        # Format the response
        formatted_data = []
        for item in paginated_data:
            timestamp = convert_timestamp(item.get("timestamp"))
            
            formatted_item = {
                "_id": str(item.get("_id", ObjectId())),
                "device_id": item.get("device_id", "main_motor"),
                "user": item.get("user", "system"),
                "status": item.get("status", False),
                "action": item.get("action", ""),
                "timestamp": timestamp.isoformat(),  # Return as ISO string for frontend
                "triggeredBy": item.get("triggeredBy", ""),
                "scheduleId": item.get("scheduleId", ""),
                "formattedTime": item.get("formattedTime", ""),
                "timezone": item.get("timezone", "UTC+8"),
                "philippine_time": item.get("philippine_time", True)
            }
            formatted_data.append(formatted_item)
        
        return formatted_data
        
    except Exception as e:
        print(f"Error in get_motor_control_history: {str(e)}")
        # Return empty array instead of error for frontend compatibility
        return []

@router.get("/motor-control/latest")
async def get_latest_motor_status():
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the motor history document
        history_doc = await collection.find_one({"_id": "motor_history"})
        
        if not history_doc:
            # Fallback: try to find any document with history array
            history_doc = await collection.find_one({"history": {"$exists": True}})
            if not history_doc:
                return []
        
        # Get the latest history entry
        history_data = history_doc.get("history", [])
        if not history_data:
            return []
        
        # Sort history by timestamp (newest first)
        def get_sort_key(item):
            timestamp = item.get("timestamp")
            converted = convert_timestamp(timestamp)
            return make_timezone_aware(converted)
        
        history_data.sort(key=get_sort_key, reverse=True)
        latest_entry = history_data[0]
        
        # Convert timestamp
        timestamp = convert_timestamp(latest_entry.get("timestamp"))
        
        # Format the response
        formatted_entry = {
            "_id": str(latest_entry.get("_id", ObjectId())),
            "device_id": latest_entry.get("device_id", "main_motor"),
            "user": latest_entry.get("user", "system"),
            "status": latest_entry.get("status", False),
            "action": latest_entry.get("action", ""),
            "timestamp": timestamp.isoformat(),  # Return as ISO string for frontend
            "triggeredBy": latest_entry.get("triggeredBy", ""),
            "scheduleId": latest_entry.get("scheduleId", ""),
            "formattedTime": latest_entry.get("formattedTime", ""),
            "timezone": latest_entry.get("timezone", "UTC+8"),
            "philippine_time": latest_entry.get("philippine_time", True)
        }
        
        return [formatted_entry]
        
    except Exception as e:
        print(f"Error in get_latest_motor_status: {str(e)}")
        # Return empty array instead of error for frontend compatibility
        return []

@router.get("/motor-control/current")
async def get_current_motor_status():
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the current status document
        current_doc = await collection.find_one({"_id": "current"})
        
        if not current_doc:
            # Fallback: try to get the latest from history
            try:
                latest_response = await get_latest_motor_status()
                if latest_response:
                    latest_entry = latest_response[0]
                    return {
                        "device_id": latest_entry.get("device_id", "main_motor"),
                        "user": latest_entry.get("user", "system"),
                        "status": latest_entry.get("status", False),
                        "action": latest_entry.get("action", ""),
                        "relatedSchedule": latest_entry.get("scheduleId", ""),
                        "formattedTime": latest_entry.get("formattedTime", ""),
                        "timestamp": latest_entry.get("timestamp"),  # Already ISO string
                        "scheduleId": latest_entry.get("scheduleId", ""),
                        "philippine_time": latest_entry.get("philippine_time", True),
                        "timezone": latest_entry.get("timezone", "UTC+8"),
                        "lastUpdated": datetime.now(timezone.utc).isoformat()
                    }
            except:
                pass
            
            # Return default values instead of error
            return {
                "device_id": "main_motor",
                "user": "system",
                "status": False,
                "action": "off",
                "relatedSchedule": "",
                "formattedTime": "",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "scheduleId": "",
                "philippine_time": True,
                "timezone": "UTC+8",
                "lastUpdated": datetime.now(timezone.utc).isoformat()
            }
        
        # Convert timestamp
        timestamp = convert_timestamp(current_doc.get("timestamp"))
        
        # Format the response
        formatted_response = {
            "device_id": current_doc.get("device_id", "main_motor"),
            "user": current_doc.get("user", "system"),
            "status": current_doc.get("status", False),
            "action": current_doc.get("action", ""),
            "relatedSchedule": current_doc.get("relatedSchedule", ""),
            "formattedTime": current_doc.get("formattedTime", ""),
            "timestamp": timestamp.isoformat(),  # Return as ISO string for frontend
            "scheduleId": current_doc.get("scheduleId", ""),
            "philippine_time": current_doc.get("philippine_time", True),
            "timezone": current_doc.get("timezone", "UTC+8"),
            "lastUpdated": datetime.now(timezone.utc).isoformat()
        }
        
        return formatted_response
        
    except Exception as e:
        print(f"Error in get_current_motor_status: {str(e)}")
        # Return default values instead of error
        return {
            "device_id": "main_motor",
            "user": "system",
            "status": False,
            "action": "off",
            "relatedSchedule": "",
            "formattedTime": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scheduleId": "",
            "philippine_time": True,
            "timezone": "UTC+8",
            "lastUpdated": datetime.now(timezone.utc).isoformat()
        }