from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()
FIREBASE_URL = os.getenv("FIREBASE_URL")

router = APIRouter()

class SMSRequest(BaseModel):
    number: str
    message: str

@router.post("/send-sms")
def send_sms(req: SMSRequest):
    if not FIREBASE_URL:
        raise HTTPException(status_code=500, detail="FIREBASE_URL is not configured")

    payload = {
        "number": req.number,
        "message": req.message,
        "sent": False,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(FIREBASE_URL, json=payload)
        response.raise_for_status()
        return {"status": "queued", "firebase_key": response.json()["name"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
