import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# Coordinates for Parang, Calapan City, Oriental Mindoro
LATITUDE = 13.401977220608616
LONGITUDE = 121.22464223345575
DATASET_PATH = "dataset.csv"

def main():
    # Check if dataset exists
    if os.path.exists(DATASET_PATH):
        existing_df = pd.read_csv(DATASET_PATH)
        last_date = pd.to_datetime(existing_df["date"].max())
        start_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        existing_df = None
        start_date = "2015-01-01"  # Default start

    end_date = datetime.now().strftime("%Y-%m-%d")

    # If start_date is today or later, skip download
    if start_date >= end_date:
        print("🟡 No new data to fetch. Dataset is already up to date.")
        return

    # Open-Meteo API URL
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"precipitation_hours,snowfall_sum,wind_speed_10m_max,cloud_cover_mean,"
        f"relative_humidity_2m_mean,surface_pressure_mean"
        f"&timezone=Asia/Manila"
    )

    response = requests.get(url)
    data = response.json()

    if "daily" in data:
        new_df = pd.DataFrame({
            "date": data["daily"]["time"],
            "temperature_max": data["daily"]["temperature_2m_max"],
            "temperature_min": data["daily"]["temperature_2m_min"],
            "rainfall": data["daily"]["precipitation_sum"],
            "precipitation_hours": data["daily"]["precipitation_hours"],
            "snowfall": data["daily"]["snowfall_sum"],
            "wind_speed": data["daily"]["wind_speed_10m_max"],
            "cloud_cover": data["daily"]["cloud_cover_mean"],
            "humidity": data["daily"]["relative_humidity_2m_mean"],
            "pressure": data["daily"]["surface_pressure_mean"]
        })

        # Combine and remove duplicates
        if existing_df is not None:
            combined_df = pd.concat([existing_df, new_df])
            combined_df.drop_duplicates(subset="date", keep="last", inplace=True)
        else:
            combined_df = new_df

        combined_df.to_csv(DATASET_PATH, index=False)
        print(f"✅ Data updated from {start_date} to {end_date} and saved to '{DATASET_PATH}'")
    else:
        print("❌ Error:", data.get("reason", "Unknown API error"))


# Optional direct run
if __name__ == "__main__":
    main()
