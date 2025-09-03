from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
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

@router.get("/motor-control/history")
async def get_motor_control_history(
    limit: int = Query(50, ge=1, le=1000),
    skip: int = Query(0, ge=0)
):
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the current document
        current_doc = await collection.find_one({"device_id": "main_motor"})
        
        if not current_doc:
            raise HTTPException(status_code=404, detail="Motor status document not found")
        
        # Extract and format history data
        history_data = current_doc.get("history", [])
        
        # Sort history by timestamp (newest first)
        history_data.sort(key=lambda x: x.get("timestamp", {}).get("_seconds", 0), reverse=True)
        
        # Apply pagination
        paginated_data = history_data[skip:skip + limit]
        
        # Format the response
        formatted_data = []
        for item in paginated_data:
            formatted_item = {
                "_id": str(item.get("_id", "")),
                "device_id": current_doc.get("device_id", "main_motor"),
                "user": current_doc.get("user", "system"),
                "status": item.get("status", False),
                "timestamp": datetime.fromtimestamp(item.get("timestamp", {}).get("_seconds", 0)),
                "triggeredBy": item.get("triggeredBy", ""),
                "scheduleId": item.get("scheduleId", "")
            }
            formatted_data.append(formatted_item)
        
        return formatted_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching motor control history: {str(e)}")

@router.get("/motor-control/latest")
async def get_latest_motor_status():
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the current document
        current_doc = await collection.find_one({"device_id": "main_motor"})
        
        if not current_doc:
            raise HTTPException(status_code=404, detail="Motor status document not found")
        
        # Get the latest history entry
        history_data = current_doc.get("history", [])
        if not history_data:
            return []
        
        # Sort history by timestamp (newest first)
        history_data.sort(key=lambda x: x.get("timestamp", {}).get("_seconds", 0), reverse=True)
        latest_entry = history_data[0]
        
        # Format the response
        formatted_entry = {
            "_id": str(latest_entry.get("_id", "")),
            "device_id": current_doc.get("device_id", "main_motor"),
            "user": current_doc.get("user", "system"),
            "status": latest_entry.get("status", False),
            "timestamp": datetime.fromtimestamp(latest_entry.get("timestamp", {}).get("_seconds", 0)),
            "triggeredBy": latest_entry.get("triggeredBy", ""),
            "scheduleId": latest_entry.get("scheduleId", "")
        }
        
        return [formatted_entry]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest motor status: {str(e)}")

@router.get("/motor-control/current")
async def get_current_motor_status():
    try:
        db = await get_database()
        collection = db["motor_status"]
        
        # Get the current document
        current_doc = await collection.find_one({"device_id": "main_motor"})
        
        if not current_doc:
            raise HTTPException(status_code=404, detail="Motor status document not found")
        
        # Get the latest history entry to determine current status
        history_data = current_doc.get("history", [])
        if history_data:
            # Sort history by timestamp (newest first)
            history_data.sort(key=lambda x: x.get("timestamp", {}).get("_seconds", 0), reverse=True)
            current_status = history_data[0].get("status", False)
        else:
            current_status = current_doc.get("status", False)
        
        # Format the response
        formatted_response = {
            "device_id": current_doc.get("device_id", "main_motor"),
            "user": current_doc.get("user", "system"),
            "status": current_status,
            "relatedSchedule": current_doc.get("relatedSchedule", ""),
            "formattedTime": current_doc.get("formattedTime", ""),
            "lastUpdated": datetime.now()
        }
        
        return formatted_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching current motor status: {str(e)}")