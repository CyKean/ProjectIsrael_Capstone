import time
import os
from datetime import datetime
from fastapi import APIRouter
from ..models.schemas import SystemInfo

router = APIRouter(prefix="/api/system", tags=["system"])

START_TIME = time.time()

@router.get("/ping", response_model=dict)
async def ping():
    """Health check endpoint"""
    return {
        "success": True,
        "version": "1.0.0",
        "uptime": int(time.time() - START_TIME),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/info", response_model=SystemInfo)
async def get_system_info():
    """Get system information"""
    return {
        "version": "1.0.0",
        "status": "running",
        "uptime": int(time.time() - START_TIME),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "last_esp32_contact": "never",  # Will be updated by ESP32 routes
        "system": {
            "python_version": os.getenv("PYTHON_VERSION", "3.9+"),
            "host": os.getenv("HOSTNAME", "localhost")
        }
    }