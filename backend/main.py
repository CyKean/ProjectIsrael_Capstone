from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import logging
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from app.routers import crop_router,auth_router,sensor_data,motor_status,water_scheduling_router,sms,esp32_ip,dashboard_router,crop_recommendation,soil_analysis,npk_router,soilph_router,soil_moisture,temhum_router,waterlevel_router,motorcontrol_router,notification_router,user_router,schedule_router,sidebar_router
from app.services.backend_ip import save_backend_ip
from app.services.esp32_ip_manager import ip_manager
from app.api.base import router as base_router
from app.api.system import router as system_router
from app.api.esp32 import router as esp32_router

from app.services.database import init_database

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set. Please check your .env file.")

save_backend_ip()

app = FastAPI(title="Crop Recommendation API")

# Enhanced CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Custom middleware to ensure CORS headers on all responses
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Add CORS headers to all responses
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Expose-Headers"] = "*"
    
    return response

# Include all routers
app.include_router(crop_router.router, prefix="/api/crop", tags=["crop"])
app.include_router(auth_router.router)
app.include_router(sensor_data.router)
app.include_router(motor_status.router)
app.include_router(water_scheduling_router.router)
app.include_router(sms.router, prefix="/api/sms", tags=["sms"])
app.include_router(esp32_ip.router)
app.include_router(base_router)
app.include_router(system_router)
app.include_router(esp32_router)
app.include_router(dashboard_router.router)
app.include_router(crop_recommendation.router)
app.include_router(soil_analysis.router)
app.include_router(npk_router.router)
app.include_router(soilph_router.router)
app.include_router(soil_moisture.router)
app.include_router(waterlevel_router.router)
app.include_router(temhum_router.router)
app.include_router(motorcontrol_router.router)
app.include_router(notification_router.router)
app.include_router(user_router.router)
app.include_router(schedule_router.router)
app.include_router(sidebar_router.router)

@app.middleware("http")
async def allow_websocket_cors(request, call_next):
    if request.scope["type"] == "websocket":
        return await sensor_data.websocket_endpoint(request)
    return await call_next(request)

# Handle OPTIONS requests for all routes
@app.options("/api/{path:path}")
async def options_handler(path: str):
    return JSONResponse(
        content={"status": "ok"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Crop Recommendation API"}

# Add health check endpoints
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "cors": "enabled"
        }
    }

@app.get("/api/health")
async def api_health_check():
    return {
        "status": "API healthy",
        "endpoints": {
            "temperature_humidity": "/api/temperature-humidity/readings"
        }
    }

# Debug endpoint to check registered routes
@app.get("/debug/routes")
async def debug_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name if hasattr(route, 'name') else 'N/A'
            })
    return {"routes": routes}

# Error handler to ensure CORS headers on errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    print(f"Unhandled exception: {exc}")
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )