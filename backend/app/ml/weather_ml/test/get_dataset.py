import requests
import csv
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API key from environment variable
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# Define location and time range
LOCATION = "Parang, Calapan City, Oriental Mindoro"
END_DATE = datetime.today()  # Today's date
START_DATE = END_DATE - timedelta(days=730)  # 2 years ago

# Define CSV file
CSV_FILE = "weather_dataset.csv"

# Function to fetch weather data for a specific date
def fetch_weather_data(date):
    url = f"https://api.weatherapi.com/v1/history.json?key={API_KEY}&q={LOCATION}&dt={date}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        weather_info = {
            "date": date,
            "location": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "temperature_c": data["forecast"]["forecastday"][0]["day"]["avgtemp_c"],
            "temperature_f": data["forecast"]["forecastday"][0]["day"]["avgtemp_f"],
            "humidity": data["forecast"]["forecastday"][0]["day"]["avghumidity"],
            "wind_speed_kph": data["forecast"]["forecastday"][0]["day"]["maxwind_kph"],
            "pressure_hpa": data["forecast"]["forecastday"][0]["hour"][0]["pressure_mb"],  # 1st hour of the day
            "cloud_cover_percent": data["forecast"]["forecastday"][0]["hour"][0]["cloud"],
            "weather_condition": data["forecast"]["forecastday"][0]["day"]["condition"]["text"],
            "rain_mm": data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],
        }
        return weather_info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {date}: {e}")
        return None

# Loop through dates and fetch data
current_date = START_DATE
file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "date", "location", "region", "country", "temperature_c", "temperature_f",
        "humidity", "wind_speed_kph", "pressure_hpa", "cloud_cover_percent",
        "weather_condition", "rain_mm"
    ])
    
    # Write headers if file doesn't exist
    if not file_exists:
        writer.writeheader()
    
    while current_date <= END_DATE:
        date_str = current_date.strftime("%Y-%m-%d")
        weather_info = fetch_weather_data(date_str)
        
        if weather_info:
            writer.writerow(weather_info)
            print(f"✅ Data saved for {date_str}")
        
        # Move to the next day
        current_date += timedelta(days=1)
        
        # Pause to avoid API rate limits
        time.sleep(1)  # Adjust if needed

print("🎉 Weather data collection complete!")



