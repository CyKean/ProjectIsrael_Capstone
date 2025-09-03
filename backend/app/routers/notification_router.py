# app/routers/notification_router.py
from datetime import datetime
from typing import List, Optional, Any, Dict
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from app.services.database import get_database

router = APIRouter(prefix="/api",tags=["notifications"])

class NotificationContext(BaseModel):
    # Flexible context structure for Firebase migrated data
    type: Optional[str] = None
    date: Optional[str] = None
    soilMoisture: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    waterLevel: Optional[float] = None
    motorStatus: Optional[str] = None
    recommendation: Optional[str] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    soilPh: Optional[float] = None
    scheduleId: Optional[str] = None
    scheduleType: Optional[str] = None
    day: Optional[int] = None
    duration: Optional[int] = None
    forecast: Optional[dict] = None
    currentWeather: Optional[dict] = None
    level: Optional[float] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    sensor1: Optional[dict] = None
    sensor2: Optional[dict] = None
    additionalInfo: Optional[str] = None

class NotificationBase(BaseModel):
    title: str
    message: str
    type: str
    severity: str = "info"
    category: Optional[str] = None
    context: Optional[dict] = None
    read: bool = False
    archived: bool = False
    archivedAt: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    read: Optional[bool] = None
    archived: Optional[bool] = None
    archivedAt: Optional[datetime] = None

class NotificationResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    message: str
    type: str
    severity: str
    category: Optional[str] = None
    context: Optional[dict] = None
    read: bool
    archived: bool
    archivedAt: Optional[datetime] = None
    timestamp: datetime
    formattedDate: Optional[str] = None
    uniqueKey: Optional[str] = None
    firebaseId: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

# Database dependency
async def get_notifications_collection():
    db = await get_database()
    return db.notifications

# Helper function to convert MongoDB document to response
def notification_helper(notification: Dict[str, Any]) -> Dict[str, Any]:
    if notification is None:
        return None
    
    # Handle Firebase migrated data - check for different ID fields
    notification_id = None
    firebase_id = None
    
    # Check for various possible ID fields from Firebase migration
    if notification.get("_id"):
        notification_id = str(notification["_id"])
    elif notification.get("id"):
        notification_id = notification["id"]
        firebase_id = notification["id"]  # This might be the original Firebase ID
    elif notification.get("documentId"):
        notification_id = notification["documentId"]
    elif notification.get("uniqueKey"):
        notification_id = notification["uniqueKey"]
    else:
        # Generate a new ID as last resort
        notification_id = str(ObjectId())
    
    # Handle timestamp conversion for Firebase format
    timestamp = notification.get("timestamp")
    if isinstance(timestamp, dict) and '_seconds' in timestamp and '_nanoseconds' in timestamp:
        # Convert Firebase timestamp to datetime
        timestamp = datetime.fromtimestamp(timestamp['_seconds'] + timestamp['_nanoseconds'] / 1e9)
    elif isinstance(timestamp, datetime):
        timestamp = timestamp
    elif isinstance(timestamp, str):
        # Try to parse string timestamp
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            timestamp = datetime.utcnow()
    else:
        timestamp = datetime.utcnow()
    
    # Handle context field - ensure it's always a dict
    context = notification.get("context", {})
    if context is None:
        context = {}
    
    # Check for explicit firebaseId field
    if notification.get("firebaseId"):
        firebase_id = notification["firebaseId"]
    
    result = {
        "_id": notification_id,
        "title": notification.get("title", ""),
        "message": notification.get("message", ""),
        "type": notification.get("type", ""),
        "severity": notification.get("severity", "info"),
        "category": notification.get("category"),
        "context": context,
        "read": notification.get("read", False),
        "archived": notification.get("archived", False),
        "archivedAt": notification.get("archivedAt"),
        "timestamp": timestamp,
        "formattedDate": notification.get("formattedDate"),
        "uniqueKey": notification.get("uniqueKey"),
        "firebaseId": firebase_id
    }
    
    # Remove any None values
    return {k: v for k, v in result.items() if v is not None}

@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    archived: Optional[bool] = Query(None),
    type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    collection = Depends(get_notifications_collection)
):
    """
    Get all notifications with optional filtering
    """
    try:
        query = {}
        if archived is not None:
            query["archived"] = archived
        if type:
            query["type"] = type
        if severity:
            query["severity"] = severity
        
        print(f"Querying notifications with filter: {query}")
        
        notifications_cursor = collection.find(query).sort("timestamp", -1)
        notifications = await notifications_cursor.to_list(length=1000)
        
        print(f"Found {len(notifications)} notifications")
        
        # Debug: Check the structure of first few documents
        if notifications and len(notifications) > 0:
            sample = notifications[0]
            print("Sample document keys:", list(sample.keys()))
            print("Sample _id:", sample.get("_id"))
            print("Sample id:", sample.get("id"))
            print("Sample timestamp:", sample.get("timestamp"))
        
        # Convert using helper function
        result = []
        seen_ids = set()
        
        for notif in notifications:
            try:
                processed_notif = notification_helper(notif)
                
                if processed_notif and processed_notif.get("_id"):
                    notification_id = processed_notif["_id"]
                    
                    if notification_id in seen_ids:
                        print(f"Duplicate ID found: {notification_id}, generating new one")
                        processed_notif["_id"] = str(ObjectId())
                    
                    seen_ids.add(processed_notif["_id"])
                    result.append(NotificationResponse(**processed_notif))
                else:
                    print(f"Skipping notification without ID: {notif}")
            except Exception as e:
                print(f"Error converting notification: {e}")
                continue
        
        print(f"Returning {len(result)} processed notifications")
        return result
    
    except Exception as e:
        print(f"Error in get_notifications: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: str,
    collection = Depends(get_notifications_collection)
):
    """
    Get a specific notification by ID
    """
    try:
        # Try ObjectId first
        if ObjectId.is_valid(notification_id):
            notification = await collection.find_one({"_id": ObjectId(notification_id)})
        else:
            # Try as string ID (for Firebase migrated IDs)
            notification = await collection.find_one({"$or": [
                {"_id": notification_id},
                {"id": notification_id},
                {"documentId": notification_id},
                {"uniqueKey": notification_id}
            ]})
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return NotificationResponse(**notification_helper(notification))
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching notification: {str(e)}")

@router.post("/notifications", response_model=NotificationResponse)
async def create_notification(
    notification: NotificationCreate,
    collection = Depends(get_notifications_collection)
):
    """
    Create a new notification
    """
    try:
        notification_data = notification.model_dump()
        notification_data["timestamp"] = datetime.utcnow()
        
        # Generate unique key if not provided
        if not notification_data.get("uniqueKey"):
            notification_data["uniqueKey"] = f"{notification.type}-{datetime.utcnow().timestamp()}"
        
        result = await collection.insert_one(notification_data)
        new_notification = await collection.find_one({"_id": result.inserted_id})
        
        return NotificationResponse(**notification_helper(new_notification))
    
    except Exception as e:
        print(f"Error in create_notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating notification: {str(e)}")

@router.patch("/notifications/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: str,
    update_data: NotificationUpdate,
    collection = Depends(get_notifications_collection)
):
    """
    Update a notification
    """
    try:
        update_fields = {k: v for k, v in update_data.model_dump().items() if v is not None}
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Try to find the document by various ID fields
        query = {"$or": [
            {"_id": ObjectId(notification_id)},
            {"_id": notification_id},
            {"id": notification_id},
            {"documentId": notification_id},
            {"uniqueKey": notification_id}
        ]} if ObjectId.is_valid(notification_id) else {"$or": [
            {"_id": notification_id},
            {"id": notification_id},
            {"documentId": notification_id},
            {"uniqueKey": notification_id}
        ]}
        
        result = await collection.update_one(query, {"$set": update_fields})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        # Get the updated document
        updated_notification = await collection.find_one(query)
        return NotificationResponse(**notification_helper(updated_notification))
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating notification: {str(e)}")

@router.delete("/notifications/{notification_id}")
async def delete_notification(
    notification_id: str,
    collection = Depends(get_notifications_collection)
):
    """
    Delete a specific notification
    """
    try:
        # Try to find and delete by various ID fields
        query = {"$or": [
            {"_id": ObjectId(notification_id)},
            {"_id": notification_id},
            {"id": notification_id},
            {"documentId": notification_id},
            {"uniqueKey": notification_id}
        ]} if ObjectId.is_valid(notification_id) else {"$or": [
            {"_id": notification_id},
            {"id": notification_id},
            {"documentId": notification_id},
            {"uniqueKey": notification_id}
        ]}
        
        result = await collection.delete_one(query)
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {"message": "Notification deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")

@router.delete("/notifications")
async def delete_all_notifications(
    collection = Depends(get_notifications_collection)
):
    """
    Delete all notifications
    """
    try:
        result = await collection.delete_many({})
        return {"message": f"Deleted {result.deleted_count} notifications"}
    
    except Exception as e:
        print(f"Error in delete_all_notifications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting all notifications: {str(e)}")

@router.post("/notifications/delete-multiple")
async def delete_multiple_notifications(
    ids: List[str] = Body(..., embed=True),
    collection = Depends(get_notifications_collection)
):
    """
    Delete multiple notifications by IDs
    """
    try:
        object_ids = []
        string_ids = []
        
        for id_str in ids:
            if ObjectId.is_valid(id_str):
                object_ids.append(ObjectId(id_str))
            else:
                string_ids.append(id_str)
        
        # Create query to match any of the ID formats
        query = {"$or": []}
        if object_ids:
            query["$or"].append({"_id": {"$in": object_ids}})
        if string_ids:
            query["$or"].extend([
                {"_id": {"$in": string_ids}},
                {"id": {"$in": string_ids}},
                {"documentId": {"$in": string_ids}},
                {"uniqueKey": {"$in": string_ids}}
            ])
        
        if not query["$or"]:
            raise HTTPException(status_code=400, detail="No valid notification IDs provided")
        
        result = await collection.delete_many(query)
        
        return {
            "message": f"Deleted {result.deleted_count} notifications",
            "deleted_count": result.deleted_count
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_multiple_notifications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting multiple notifications: {str(e)}")

@router.post("/notifications/mark-all-read")
async def mark_all_notifications_read(
    collection = Depends(get_notifications_collection)
):
    """
    Mark all notifications as read
    """
    try:
        result = await collection.update_many(
            {"read": False},
            {"$set": {"read": True}}
        )
        
        return {"message": f"Marked {result.modified_count} notifications as read"}
    
    except Exception as e:
        print(f"Error in mark_all_notifications_read: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error marking notifications as read: {str(e)}")

@router.get("/notifications/unread/count")
async def get_unread_count(
    collection = Depends(get_notifications_collection)
):
    """
    Get count of unread notifications
    """
    try:
        count = await collection.count_documents({"read": False, "archived": False})
        return {"unread_count": count}
    
    except Exception as e:
        print(f"Error in get_unread_count: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting unread count: {str(e)}")

# Debug endpoint to check data structure
@router.get("/notifications/debug/structure")
async def debug_structure(
    collection = Depends(get_notifications_collection)
):
    """
    Debug endpoint to check notification data structure
    """
    try:
        sample = await collection.find_one({})
        if not sample:
            return {"message": "No notifications found", "sample": None}
        
        return {
            "keys": list(sample.keys()),
            "sample_id": str(sample.get("_id")) if sample.get("_id") else sample.get("id"),
            "timestamp_type": type(sample.get("timestamp")).__name__,
            "has_context": "context" in sample,
            "sample_data": {k: str(type(v).__name__) for k, v in sample.items()}
        }
    except Exception as e:
        return {"error": str(e)}