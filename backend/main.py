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
from app.routers import crop_router, auth_router, sensor_data, notif, motor_status, water_scheduling_router, esp1, esp2, esp3, sms, esp32_ip
# sms, otp
from app.ml.weather_ml.forecast.forecast import main as run_forecast
# from app.ml.weather_ml.forecast.get_dataset import main as update_dataset
from app.services.backend_ip import save_backend_ip
from app.services.esp32_ip_manager import ip_manager
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
    "http://localhost:3000",
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
app.include_router(sensor_data.router)
app.include_router(notif.router)
app.include_router(motor_status.router)
app.include_router(water_scheduling_router.router)
app.include_router(sms.router, prefix="/api/sms", tags=["sms"])
# app.include_router(otp.router)
app.include_router(esp1.router)
app.include_router(esp2.router)
app.include_router(esp3.router)
app.include_router(esp32_ip.router)



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
    





# from fastapi import FastAPI, HTTPException, Request, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# import os
# import httpx
# import logging
# from dotenv import load_dotenv
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# import requests  # <-- ADDED

# # Custom module imports
# from app.services.firebase_service import firebase_admin
# from app.routers import crop_router, auth_router, sensor_data, notif, motor_status, water_scheduling_router, esp1, esp2, esp3, otp, sms
# from app.ml.weather_ml.forecast.forecast import main as run_forecast
# from app.services.backend_ip import save_backend_ip

# # ======== ENV & LOG SETUP =========
# load_dotenv()
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
# if not WEATHER_API_KEY:
#     raise ValueError("WEATHER_API_KEY is not set. Please check your .env file.")

# save_backend_ip()

# # ======== SEND SMS MESSAGE VIA TELEGRAM BOT =========
# import os
# import requests
# import logging
# from urllib.parse import quote

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def send_sms_via_telegram(bot_token, chat_id, phone_number, message_text):
#     """Send SMS-style message to Telegram bot with proper escaping"""
#     try:
#         # Format the message exactly as requested
#         formatted_message = f"/sms {phone_number} {message_text}"
        
#         # URL encode the message for safety
#         encoded_message = quote(formatted_message)
        
#         # Using GET request instead of POST for better error visibility
#         response = requests.get(
#             f"https://api.telegram.org/bot{bot_token}/sendMessage",
#             params={
#                 "chat_id": chat_id,
#                 "text": formatted_message,
#                 "disable_web_page_preview": True
#             },
#             timeout=10
#         )
        
#         # More detailed error response parsing
#         if response.status_code != 200:
#             error_info = response.json()
#             logging.error(f"Telegram API error: {error_info.get('description', 'Unknown error')}")
#             if 'parameters' in error_info:
#                 logging.error(f"Error details: {error_info['parameters']}")
#             return False
            
#         logging.info(f"SMS message sent to {phone_number}")
#         return True
        
#     except Exception as e:
#         logging.error(f"Failed to send SMS via Telegram: {str(e)}", exc_info=True)
#         return False

# # Get environment variables
# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "7961729220:AAFKIdgCFtNuMjlkuQssqUBZLjeXTmYIhnY"
# TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "6085990774"

# if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
#     # Example usage with your requested format
#     phone_number = "+639627080157"  # Replace with actual phone number
#     otp_code = "481317"            # Replace with generated OTP
#     message_content = f"Your OTP code is: {otp_code}"
    
#     if not send_sms_via_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, phone_number, message_content):
#         logging.warning("Failed to send SMS message via Telegram")
# else:
#     logging.warning("Telegram credentials not configured - cannot send SMS message")

# # ======== FASTAPI APP SETUP =========
# app = FastAPI(title="Crop Recommendation API")

# # ======== CORS CONFIG =========
# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ======== ROUTERS =========
# app.include_router(crop_router.router, prefix="/api/crop", tags=["crop"])
# app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
# app.include_router(sensor_data.router)
# app.include_router(notif.router)
# app.include_router(motor_status.router)
# app.include_router(water_scheduling_router.router)
# app.include_router(sms.router)
# app.include_router(otp.router)
# app.include_router(esp1.router)
# app.include_router(esp2.router)
# app.include_router(esp3.router)

# # ======== MIDDLEWARE FOR WS =========
# @app.middleware("http")
# async def allow_websocket_cors(request, call_next):
#     if request.scope["type"] == "websocket":
#         return await sensor_data.websocket_endpoint(request)
#     return await call_next(request)

# # ======== ROUTES =========
# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Crop Recommendation API"}

# @app.get("/firebase-test")
# async def firebase_test():
#     if firebase_admin:
#         return {"message": "Firebase is initialized successfully"}
#     return {"error": "Firebase initialization failed"}

# @app.get("/weather/")
# async def get_weather():
#     latitude = 13.401977220608616
#     longitude = 121.22464223345575
#     coordinates = f"{latitude},{longitude}"

#     params = {
#         "key": WEATHER_API_KEY,
#         "q": coordinates,
#         "aqi": "no"
#     }

#     try:
#         async with httpx.AsyncClient(timeout=10.0) as client:
#             response = await client.get("http://api.weatherapi.com/v1/current.json", params=params)
#             response.raise_for_status()
#     except httpx.RequestError as e:
#         raise HTTPException(status_code=500, detail=f"Weather API error: {e}")

#     weather_data = response.json()
#     wind_speed_kph = weather_data["current"]["wind_kph"]
#     wind_speed_ms = round(wind_speed_kph / 3.6, 2)

#     return {
#         "location": weather_data["location"]["name"],
#         "region": weather_data["location"]["region"],
#         "country": weather_data["location"]["country"],
#         "temperature_c": weather_data["current"]["temp_c"],
#         "temperature_f": weather_data["current"]["temp_f"],
#         "humidity": weather_data["current"]["humidity"],
#         "wind_speed_kph": wind_speed_kph,
#         "wind_speed_ms": wind_speed_ms,
#         "pressure_hpa": weather_data["current"]["pressure_mb"],
#         "cloud_cover_percent": weather_data["current"]["cloud"],
#         "weather_condition": weather_data["current"]["condition"]["text"],
#         "rain_mm": weather_data["current"].get("precip_mm", 0),
#         "uv": weather_data["current"].get("uv", 0),
#         "last_updated": weather_data["current"].get("last_updated")
#     }
