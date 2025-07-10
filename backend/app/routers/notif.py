from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from firebase_admin import firestore
from app.services.firebase_config import db

router = APIRouter(prefix='/api')

class Notification(BaseModel):
    id: str
    title: str
    message: str
    type: str
    severity: str  # New field: 'info', 'warning', 'alert', 'critical', etc.
    timestamp: datetime
    read: bool = False

@router.post("/notifications")
async def create_notification(notification: Notification):
    try:
        data = notification.dict()
        if not data.get("timestamp"):
            data["timestamp"] = datetime.utcnow()
        db.collection("notifications").document(notification.id).set(data)
        return {"message": "Notification saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-notifications")
async def get_notifications():
    try:
        docs = db.collection("notifications").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications/{notification_id}/read")
async def mark_notification_as_read(notification_id: str):
    try:
        db.collection("notifications").document(notification_id).update({"read": True})
        return {"message": "Notification marked as read"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications/read-all")
async def mark_all_notifications_as_read():
    try:
        notifications_ref = db.collection("notifications").where("read", "==", False)
        batch = db.batch()

        for doc in notifications_ref.stream():
            batch.update(doc.reference, {"read": True})

        batch.commit()
        return {"message": "All notifications marked as read"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))