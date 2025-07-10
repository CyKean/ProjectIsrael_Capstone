# import requests
# import pandas as pd

# # Coordinates for Parang, Calapan City, Oriental Mindoro
# LATITUDE = 13.3895  # Corrected to the specified location
# LONGITUDE = 121.2312  # Corrected to the specified location

# # Date range for 1 to 2 years
# start_date = "2022-01-01"
# end_date = "2025-03-07"

# # Open-Meteo archive API endpoint with supported variables
# url = f"https://archive-api.open-meteo.com/v1/archive?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,cloud_cover_mean&timezone=Asia/Manila"

# # Send GET request to Open-Meteo API
# response = requests.get(url)

# # Parse the JSON response
# data = response.json()

# # Check if the "daily" key exists in the response
# if "daily" in data:
#     # Create a DataFrame from the weather data
#     df = pd.DataFrame({
#         "date": data["daily"]["time"],
#         "temperature_max": data["daily"]["temperature_2m_max"],
#         "temperature_min": data["daily"]["temperature_2m_min"],
#         "rainfall": data["daily"]["precipitation_sum"],
#         "wind_speed": data["daily"]["wind_speed_10m_max"],
#         "cloud_cover": data["daily"]["cloud_cover_mean"]
#     })
    
#     # Save the data to a CSV file
#     df.to_csv("weather_data_parang_calapan.csv", index=False)
#     print("✅ Weather data saved to 'weather_data_parang_calapan.csv'!")

# else:
#     # If the "daily" key is not found, print the error message
#     print("❌ API did not return expected weather data:", data)



import requests
import pandas as pd
from datetime import datetime

# Coordinates for Parang, Calapan City, Oriental Mindoro
LATITUDE = 13.3895
LONGITUDE = 121.2312

# Date range from 2015 to current date
start_date = "2015-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")

# Updated API request with additional precipitation parameters
url = f"https://archive-api.open-meteo.com/v1/archive?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours,snowfall_sum,wind_speed_10m_max,cloud_cover_mean,relative_humidity_2m_mean,surface_pressure_mean&timezone=Asia/Manila"

response = requests.get(url)
data = response.json()

if "daily" in data:
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temperature_max": data["daily"]["temperature_2m_max"],
        "temperature_min": data["daily"]["temperature_2m_min"],
        "rainfall": data["daily"]["precipitation_sum"],
        "precipitation_hours": data["daily"]["precipitation_hours"],  # New
        "snowfall": data["daily"]["snowfall_sum"],  # New (likely 0s in PH)
        "wind_speed": data["daily"]["wind_speed_10m_max"],
        "cloud_cover": data["daily"]["cloud_cover_mean"],
        "humidity": data["daily"]["relative_humidity_2m_mean"],
        "pressure": data["daily"]["surface_pressure_mean"]
    })
    
    df.to_csv("weather_data.csv", index=False)
    print(f"✅ Historical data ({start_date} to {end_date}) saved successfully!")
else:
    print("❌ Error:", data.get("reason", "Unknown API error"))


# VisualCrossing
# import requests
# import pandas as pd
# from datetime import datetime, timedelta
# import time

# # Coordinates for Parang, Calapan City, Oriental Mindoro
# LATITUDE = 13.3895
# LONGITUDE = 121.2312

# # Set the date range: last 5 years
# end_date = datetime.today()
# start_date = end_date - timedelta(days=365*5)  # 5 years back

# # Visual Crossing API URL
# API_KEY = "Q7ZEY7BBF9VVLLAHKZN8T8SDM"  # Replace with your API key
# BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# # Function to fetch weather data for a specific date range
# def fetch_weather_data(start_date, end_date):
#     url = f"{BASE_URL}/{LATITUDE},{LONGITUDE}/{start_date}/{end_date}?key={API_KEY}&include=temperature,humidity,precipitation,pressure,windSpeed"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         return data
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching data from {start_date} to {end_date}: {e}")
#         return None

# # Function to split the date range into 60-day intervals
# def split_date_range(start_date, end_date):
#     date_ranges = []
#     current_start = start_date

#     while current_start < end_date:
#         current_end = current_start + timedelta(days=60)  # Add 60 days
#         if current_end > end_date:
#             current_end = end_date  # Ensure the end date does not exceed the total range
#         date_ranges.append((current_start, current_end))
#         current_start = current_end + timedelta(days=1)  # Move to the next chunk

#     return date_ranges

# # Function to save data to CSV
# def save_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)
#     print(f"✅ Data saved to {filename}")

# # Prepare for collecting the weather data
# date_ranges = split_date_range(start_date, end_date)
# all_data = []

# # Fetch weather data in 60-day chunks
# for start, end in date_ranges:
#     print(f"Fetching data from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}...")
#     weather_data = fetch_weather_data(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

#     if weather_data and "days" in weather_data:
#         daily_data = weather_data["days"]
#         for day in daily_data:
#             all_data.append({
#                 "date": day["datetime"],
#                 "temperature_max": day.get("tempmax", None),
#                 "temperature_min": day.get("tempmin", None),
#                 "precipitation": day.get("precip", None),
#                 "wind_speed": day.get("windspeed", None),
#                 "cloud_cover": day.get("cloudcover", None),  # Cloud cover might not be available for all data points
#                 "humidity_max": day.get("humiditymax", None),  # Safe access
#                 "pressure": day.get("pressure", None)  # Safe access
#             })

#     # Sleep to avoid exceeding API request limits
#     time.sleep(1)

# # Save the combined data into a CSV
# save_to_csv(all_data, "historical_weather_data.csv")




# # WeatherStack
# import requests
# import pandas as pd
# from datetime import datetime, timedelta

# # Coordinates for Parang, Calapan City, Oriental Mindoro
# LATITUDE = 13.3895
# LONGITUDE = 121.2312
# API_KEY = "045f471ef06ef06cd7fa6ee32be5f418"  # Replace with your Weatherstack API key

# # Set the date range: last 10 years
# end_date = datetime.today()
# start_date = end_date - timedelta(days=365*10)  # 10 years back

# # Weatherstack API URL for historical data
# BASE_URL = "http://api.weatherstack.com/historical"

# # Function to fetch historical weather data for a specific date
# def fetch_weather_data(date):
#     url = f"{BASE_URL}?access_key={API_KEY}&query={LATITUDE},{LONGITUDE}&historical_date={date}&hourly=temperature_2m,precipitation,wind_speed_10m,cloudcover,humidity_2m,pressure_msl"
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Print full response for debugging
#         print(f"Response for {date}: {response.json()}")
#         return response.json()
#     else:
#         print(f"❌ Error fetching data for {date}: {response.status_code}")
#         return None

# # Function to save the data to CSV
# def save_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)
#     print(f"✅ Data saved to {filename}")

# # Collect historical data for the last 10 years
# all_data = []
# current_date = start_date
# while current_date <= end_date:
#     date_str = current_date.strftime('%Y-%m-%d')
#     print(f"Fetching data for {date_str}...")
#     weather_data = fetch_weather_data(date_str)
    
#     if weather_data and "historical" in weather_data:
#         day_data = weather_data["historical"]
#         for day in day_data.values():
#             all_data.append({
#                 "date": date_str,
#                 "temperature_max": day.get("temperature_2m_max", None),
#                 "temperature_min": day.get("temperature_2m_min", None),
#                 "precipitation": day.get("precipitation", None),
#                 "wind_speed": day.get("wind_speed_10m", None),
#                 "cloud_cover": day.get("cloudcover", None),
#                 "humidity_max": day.get("humidity_2m_max", None),
#                 "pressure": day.get("pressure_msl", None)
#             })
    
#     current_date += timedelta(days=1)  # Move to the next day

# # Save the collected data to a CSV file
# if all_data:
#     save_to_csv(all_data, "historical_weather_data.csv")
# else:
#     print("❌ No data to save.")





# open-meteo
# import requests
# import pandas as pd
# from datetime import datetime, timedelta

# # Coordinates for Parang, Calapan City, Oriental Mindoro
# LATITUDE = 13.3895
# LONGITUDE = 121.2312

# # Set the date range: last 10 years
# end_date = datetime.today()
# start_date = end_date - timedelta(days=365*10)  # 10 years back

# # Open-Meteo API URL for historical data
# BASE_URL = "https://api.open-meteo.com/v1/forecast"

# # Function to fetch historical weather data for a specific date range
# def fetch_weather_data(start_date, end_date):
#     url = f"{BASE_URL}?latitude={LATITUDE}&longitude={LONGITUDE}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,cloudcover,humidity_2m_max,pressure_msl&start_date={start_date}&end_date={end_date}&timezone=auto"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"❌ Error fetching data from {start_date} to {end_date}: {response.status_code}")
#         return None

# # Function to save data to CSV
# def save_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)
#     print(f"✅ Data saved to {filename}")

# # Function to split the date range into smaller chunks (no more than 7 days per request)
# def split_date_range(start_date, end_date, chunk_size=7):
#     date_ranges = []
#     current_start = start_date

#     while current_start < end_date:
#         current_end = current_start + timedelta(days=chunk_size)
#         if current_end > end_date:
#             current_end = end_date
#         date_ranges.append((current_start, current_end))
#         current_start = current_end + timedelta(days=1)  # Move to the next chunk

#     return date_ranges

# # Prepare for collecting the weather data
# date_ranges = split_date_range(start_date, end_date)
# all_data = []

# # Fetch weather data in chunks
# for start, end in date_ranges:
#     start_str = start.strftime('%Y-%m-%d')
#     end_str = end.strftime('%Y-%m-%d')
#     print(f"Fetching data from {start_str} to {end_str}...")
#     weather_data = fetch_weather_data(start_str, end_str)

#     if weather_data and "daily" in weather_data:
#         daily_data = weather_data["daily"]
#         for i in range(len(daily_data["time"])):
#             all_data.append({
#                 "date": daily_data["time"][i],
#                 "temperature_max": daily_data["temperature_2m_max"][i],
#                 "temperature_min": daily_data["temperature_2m_min"][i],
#                 "precipitation": daily_data["precipitation_sum"][i],
#                 "wind_speed": daily_data["wind_speed_10m_max"][i],
#                 "cloud_cover": daily_data["cloudcover"][i],
#                 "humidity_max": daily_data["humidity_2m_max"][i],
#                 "pressure": daily_data["pressure_msl"][i]
#             })
    
# # Save the combined data into a CSV
# if all_data:
#     save_to_csv(all_data, "historical_weather_data.csv")
# else:
#     print("❌ No data to save.")





# # weatherbit
# import requests
# import pandas as pd
# from datetime import datetime, timedelta
# import time

# # Coordinates for Parang, Calapan City, Oriental Mindoro
# LATITUDE = 13.3895
# LONGITUDE = 121.2312

# # Weatherbit API URL for historical data
# API_KEY = "70f332caad6c46c6aa56f9143c216bc3"  # Replace with your Weatherbit API key
# BASE_URL = "https://api.weatherbit.io/v2.0/history/daily"

# # Set the date range: last 10 years
# end_date = datetime.today()
# start_date = end_date - timedelta(days=365*10)  # 10 years back

# # Function to fetch historical weather data for a specific date range
# def fetch_weather_data(start_date, end_date):
#     url = f"{BASE_URL}?lat={LATITUDE}&lon={LONGITUDE}&start_date={start_date}&end_date={end_date}&key={API_KEY}&include=temperature,humidity,precipitation,pressure,wind_speed"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"❌ Error fetching data from {start_date} to {end_date}: {response.status_code}")
#         return None

# # Function to save data to CSV
# def save_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)
#     print(f"✅ Data saved to {filename}")

# # Function to split the date range into smaller chunks (no more than 15 days per request)
# def split_date_range(start_date, end_date, chunk_size=15):
#     date_ranges = []
#     current_start = start_date

#     while current_start < end_date:
#         current_end = current_start + timedelta(days=chunk_size)
#         if current_end > end_date:
#             current_end = end_date
#         date_ranges.append((current_start, current_end))
#         current_start = current_end + timedelta(days=1)  # Move to the next chunk

#     return date_ranges

# # Prepare for collecting the weather data
# date_ranges = split_date_range(start_date, end_date)
# all_data = []

# # Fetch weather data in chunks
# for start, end in date_ranges:
#     start_str = start.strftime('%Y-%m-%d')
#     end_str = end.strftime('%Y-%m-%d')
#     print(f"Fetching data from {start_str} to {end_str}...")
#     weather_data = fetch_weather_data(start_str, end_str)

#     if weather_data and "data" in weather_data:
#         daily_data = weather_data["data"]
#         for day in daily_data:
#             all_data.append({
#                 "date": day["datetime"],
#                 "temperature_max": day.get("max_temp", None),
#                 "temperature_min": day.get("min_temp", None),
#                 "precipitation": day.get("precip", None),
#                 "wind_speed": day.get("windspeed", None),
#                 "cloud_cover": day.get("clouds", None),
#                 "humidity_max": day.get("rh_max", None),
#                 "pressure": day.get("pres", None)
#             })
    
#     # Sleep for 5 seconds to avoid hitting API rate limits
#     time.sleep(5)

# # Save the combined data into a CSV
# if all_data:
#     save_to_csv(all_data, "historical_weather_data_weatherbit.csv")
# else:
#     print("❌ No data to save.")





# import requests
# import csv
# import time

# # WeatherAPI endpoint
# API_URL = "https://api.weatherapi.com/v1/history.json"
# API_KEY = "YOUR_A13a37e2f6ce24c979c7124002250503PI_KEY"  # Replace with your actual API key
# LATITUDE = 13.3895
# LONGITUDE = 121.2312

# # Function to fetch weather data for a specific date
# def fetch_weather_data(date):
#     url = f"{API_URL}?key={API_KEY}&q={LATITUDE},{LONGITUDE}&dt={date}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Check for HTTP errors
#         return response.json()  # Return the response as a dictionary
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching data for {date}: {e}")
#         return None

# # Function to save weather data to a CSV file
# def save_data_to_csv(data, filename='historical_weather_data.csv'):
#     with open(filename, mode='a', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=["date", "temperature_max", "temperature_min", "precipitation", "wind_speed", "cloud_cover", "humidity", "pressure"])
#         # Write header only if the file is empty
#         if file.tell() == 0:
#             writer.writeheader()
#         writer.writerows(data)

# # Function to handle the chunked fetching of data for 10 years
# def get_historical_data(start_date, end_date, chunk_size=60):
#     all_data = []
#     current_date = start_date

#     while current_date <= end_date:
#         # Format the date in YYYY-MM-DD format
#         print(f"Fetching data for {current_date}...")
        
#         # Fetch weather data for the current date
#         data = fetch_weather_data(current_date)
#         if data:
#             # Extract the weather data (adjust this according to your needs)
#             day_data = {
#                 "date": current_date,
#                 "temperature_max": data["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
#                 "temperature_min": data["forecast"]["forecastday"][0]["day"]["mintemp_c"],
#                 "precipitation": data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],
#                 "wind_speed": data["forecast"]["forecastday"][0]["day"]["maxwind_kph"],
#                 "cloud_cover": data["forecast"]["forecastday"][0]["day"]["avghumidity"],
#                 "humidity": data["forecast"]["forecastday"][0]["day"]["avghumidity"],
#                 "pressure": data["forecast"]["forecastday"][0]["day"]["pressure_mb"]
#             }
#             all_data.append(day_data)
        
#         # Save data to CSV in chunks
#         if len(all_data) >= chunk_size:
#             save_data_to_csv(all_data)
#             all_data = []  # Reset the list for the next chunk
        
#         # Move to the next day (for simplicity, we're just incrementing the day)
#         time.sleep(1)  # Respect the rate limit; adjust as needed
#         current_date = increment_date_by_one_day(current_date)  # Define this function to increment the date

#     # Save any remaining data after the loop
#     if all_data:
#         save_data_to_csv(all_data)

# # Function to increment the date by one day
# def increment_date_by_one_day(date):
#     from datetime import datetime, timedelta
#     date_obj = datetime.strptime(date, "%Y-%m-%d")
#     new_date_obj = date_obj + timedelta(days=1)
#     return new_date_obj.strftime("%Y-%m-%d")

# # Run the function with your start and end dates
# start_date = "2015-03-11"
# end_date = "2015-03-16"  # Update this to your desired range
# get_historical_data(start_date, end_date)
