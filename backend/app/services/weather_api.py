import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") 

async def get_weather():
    location = "Parang, Calapan City, Oriental Mindoro"

    params = {
        "key": WEATHER_API_KEY,
        "q": location,
        "aqi": "no"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("http://api.weatherapi.com/v1/current.json", params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")

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
    }
