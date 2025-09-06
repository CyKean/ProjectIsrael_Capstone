from fastapi import APIRouter, HTTPException
import time
from datetime import datetime

# Create the router object
router = APIRouter(prefix="/api/system", tags=["system"])

# Store startup time for uptime calculation
startup_time = time.time()

@router.get("/ping")
async def system_ping():
    """
    Health check endpoint for the backend system
    """
    try:
        return {
            "success": True,
            "message": "Backend is running",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",  # You can make this dynamic
            "uptime": int(time.time() - startup_time)  # seconds since startup
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")

@router.get("/info")
async def system_info():
    """
    Get system information
    """
    try:
        return {
            "status": "running",
            "version": "1.0.0",
            "uptime": int(time.time() - startup_time),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")

# Export the router object for consistent import pattern
__all__ = ['router']