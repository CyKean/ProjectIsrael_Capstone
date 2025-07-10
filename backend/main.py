from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Custom module imports
from app.services.firebase_service import firebase_admin
from app.routers import crop_router, auth_router, sensor_data, notif, motor_status, water_scheduling_router, esp1, esp2, esp3
# sms, otp
from app.ml.weather_ml.forecast.forecast import main as run_forecast
# from app.ml.weather_ml.forecast.get_dataset import main as update_dataset
from app.services.backend_ip import save_backend_ip

# ======== ENV & LOG SETUP =========
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set. Please check your .env file.")

save_backend_ip()

# ======== FASTAPI APP SETUP =========
app = FastAPI(title="Crop Recommendation API")

# ======== CORS CONFIG =========
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======== ROUTERS =========
app.include_router(crop_router.router, prefix="/api/crop", tags=["crop"])
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
# app.include_router(forecast_router.router, prefix="/api/weather", tags=["weather"])
# app.include_router(npk_router.router, prefix="/api/npk", tags=["npk"])
app.include_router(sensor_data.router)
app.include_router(notif.router)
app.include_router(motor_status.router)
app.include_router(water_scheduling_router.router)
# app.include_router(sms.router)
# app.include_router(otp.router)
# app.include_router(forecast.router)
app.include_router(esp1.router)
app.include_router(esp2.router)
app.include_router(esp3.router)



# ======== MIDDLEWARE FOR WS =========
@app.middleware("http")
async def allow_websocket_cors(request, call_next):
    if request.scope["type"] == "websocket":
        return await sensor_data.websocket_endpoint(request)
    return await call_next(request)

# ======== ROUTES =========
@app.get("/")
async def root():
    return {"message": "Welcome to the Crop Recommendation API"}

@app.get("/firebase-test")
async def firebase_test():
    if firebase_admin:
        return {"message": "Firebase is initialized successfully"}
    return {"error": "Firebase initialization failed"}

@app.get("/weather/")
async def get_weather():
    latitude = 13.401977220608616
    longitude = 121.22464223345575
    coordinates = f"{latitude},{longitude}"

    params = {
        "key": WEATHER_API_KEY,
        "q": coordinates,
        "aqi": "no"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://api.weatherapi.com/v1/current.json", params=params)
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {e}")

    weather_data = response.json()
    wind_speed_kph = weather_data["current"]["wind_kph"]
    wind_speed_ms = round(wind_speed_kph / 3.6, 2)

    return {
        "location": weather_data["location"]["name"],
        "region": weather_data["location"]["region"],
        "country": weather_data["location"]["country"],
        "temperature_c": weather_data["current"]["temp_c"],
        "temperature_f": weather_data["current"]["temp_f"],
        "humidity": weather_data["current"]["humidity"],
        "wind_speed_kph": wind_speed_kph,
        "wind_speed_ms": wind_speed_ms,
        "pressure_hpa": weather_data["current"]["pressure_mb"],
        "cloud_cover_percent": weather_data["current"]["cloud"],
        "weather_condition": weather_data["current"]["condition"]["text"],
        "rain_mm": weather_data["current"].get("precip_mm", 0),
        "uv": weather_data["current"].get("uv", 0),
        "last_updated": weather_data["current"].get("last_updated")
    }

# ======== SENSOR DATA ROUTE (for ESP32) =========
# @app.post("/sensor-data")
# async def receive_sensor_data(request: Request):
#     try:
#         data = await request.json()
#         print("✅ Sensor data received from ESP32:", data)
#         return {"message": "Data received successfully"}
#     except Exception as e:
#         print("❌ Error parsing sensor data:", str(e))
#         raise HTTPException(status_code=400, detail="Invalid JSON")
    
