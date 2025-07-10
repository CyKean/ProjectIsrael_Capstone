# import requests
# import pandas as pd
# import numpy as np
# import os
# import tensorflow as tf
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# from dotenv import load_dotenv
# from datetime import datetime

# # Load API key from environment variable
# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")

# # Coordinates for Parang, Calapan City, Oriental Mindoro
# LOCATION = "Parang, Calapan City, Oriental Mindoro"
# LATITUDE = 13.3895
# LONGITUDE = 121.2312

# # Use today's date for API request
# end_date = datetime.today().strftime('%Y-%m-%d')

# # WeatherAPI endpoint for current weather
# url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}"

# # Fetch current weather data
# url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}&aqi=yes"
# response = requests.get(url)
# current_weather = response.json()

# # Fetch forecast for moon phase
# forecast_url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days=1"
# forecast_response = requests.get(forecast_url)
# forecast_data = forecast_response.json()

# # Fetch current weather data
# try:
#     response = requests.get(url, timeout=10)
#     response.raise_for_status()
#     current_weather = response.json()
# except requests.exceptions.RequestException as e:
#     print(f"❌ Error fetching current weather data: {e}")
#     exit()

# # Extract relevant data
# current_conditions = current_weather.get('current', {})
# temperature = current_conditions.get('temp_c', np.nan)
# wind_speed = current_conditions.get('wind_kph', np.nan) * 0.277778  # Convert km/h to m/s
# humidity = current_conditions.get('humidity', np.nan)
# dew_point = current_conditions.get('dewpoint_c', np.nan)
# pressure = current_conditions.get('pressure_mb', np.nan) * 100  # Convert mb to Pa
# uv_index = current_conditions.get('uv', 'N/A')  # Avoid NaN values
# visibility = current_conditions.get('vis_km', np.nan) * 1000  # Convert km to meters
# moon_phase = forecast_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {}).get('moon_phase', 'N/A')
# air_quality_index = current_conditions.get('air_quality', {}).get('us-epa-index', 'N/A')

# # Print extracted data
# print("\nExtracted Weather Data:")
# print(f"Temperature: {temperature}°C")
# print(f"Wind Speed: {wind_speed} m/s")
# print(f"Humidity: {humidity}%")
# print(f"Dew Point: {dew_point}°C")
# print(f"Pressure: {pressure} Pa")
# print(f"UV Index: {uv_index}")
# print(f"Visibility: {visibility} meters")
# print(f"Moon Phase: {moon_phase}")
# print(f"Air Quality Index: {air_quality_index}")

# # Date range for historical data
# start_date = "2022-01-01"

# # Open-Meteo API endpoint
# url = f"https://archive-api.open-meteo.com/v1/archive?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,cloud_cover_mean&timezone=Asia/Manila"

# # Fetch historical weather data
# try:
#     response = requests.get(url, timeout=15)
#     response.raise_for_status()
#     data = response.json()
# except requests.exceptions.RequestException as e:
#     print(f"❌ Error fetching historical weather data: {e}")
#     exit()

# if "daily" in data:
#     df = pd.DataFrame({
#         "date": data["daily"]["time"],
#         "temperature_max": data["daily"]["temperature_2m_max"],
#         "temperature_min": data["daily"]["temperature_2m_min"],
#         "rainfall": data["daily"]["precipitation_sum"],
#         "wind_speed": data["daily"]["wind_speed_10m_max"],
#         "cloud_cover": data["daily"]["cloud_cover_mean"]
#     })

#     df['date'] = pd.to_datetime(df['date'])
#     df.set_index('date', inplace=True)
#     df.fillna(method='ffill', inplace=True)

#     df['month'] = df.index.month
#     df['day'] = df.index.day

#     scaler = StandardScaler()
#     features = ['temperature_max', 'temperature_min', 'rainfall', 'wind_speed', 'cloud_cover']
#     df[features] = scaler.fit_transform(df[features])

#     X = df[features].values
#     y = df[features].shift(-1).dropna().values
#     X = X[:-1]

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

#     X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
#     X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

#     model = Sequential([
#         LSTM(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
#         Dense(5)
#     ])
#     model.compile(optimizer='adam', loss='mean_squared_error')
#     model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

#     loss = model.evaluate(X_test, y_test)
#     print(f"Test loss: {loss}")

#     forecast = []
#     last_data = X[-1].reshape(1, 1, X.shape[1])
#     for _ in range(30):
#         predicted = model.predict(last_data)
#         forecast.append(predicted[0])
#         last_data = np.roll(last_data, -1, axis=2)
#         last_data[0, 0, -1] = predicted[0][-1]

#     forecast = np.array(forecast)
#     forecast_values = scaler.inverse_transform(forecast)
#     forecast_df = pd.DataFrame({
#         'date': pd.date_range(start=end_date, periods=30, freq='D'),
#         'temperature_max': forecast_values[:, 0],
#         'temperature_min': forecast_values[:, 1],
#         'rainfall': forecast_values[:, 2],
#         'wind_speed': forecast_values[:, 3],
#         'cloud_cover': forecast_values[:, 4]
#     })
    
#     forecast_df.to_csv('forecasted_weather_data.csv', index=False)
#     print("✅ Weather forecast saved to 'forecasted_weather_data.csv'!")
# else:
#     print("❌ API did not return expected weather data.")


import requests
import pandas as pd
import numpy as np
import os
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from dotenv import load_dotenv
from datetime import datetime
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error


# Load API key from environment variable
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# Coordinates for Parang, Calapan City, Oriental Mindoro
LOCATION = "Parang, Calapan City, Oriental Mindoro"
LATITUDE = 13.3895
LONGITUDE = 121.2312

# Use today's date for API request
end_date = datetime.today().strftime('%Y-%m-%d')

# WeatherAPI endpoints
current_weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}&aqi=yes"
forecast_url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days=1"

# Fetch current weather data
try:
    response = requests.get(current_weather_url, timeout=10)
    response.raise_for_status()
    current_weather = response.json()
except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching current weather data: {e}")
    exit()

# Fetch forecast for moon phase
try:
    forecast_response = requests.get(forecast_url, timeout=10)
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()
except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching forecast data: {e}")
    exit()

# Extract relevant weather data
current_conditions = current_weather.get('current', {})

temperature = current_conditions.get('temp_c', np.nan)
wind_speed = current_conditions.get('wind_kph', np.nan) * 0.277778  # Convert km/h to m/s
humidity = current_conditions.get('humidity', np.nan)
dew_point = current_conditions.get('dewpoint_c', np.nan)
pressure = current_conditions.get('pressure_mb', np.nan) * 100  # Convert mb to Pa
uv_index = current_conditions.get('uv', np.nan)  # Avoid NaN values
visibility = current_conditions.get('vis_km', np.nan) * 1000  # Convert km to meters
moon_phase = forecast_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {}).get('moon_phase', 'N/A')

# Extract air quality index correctly
air_quality = current_conditions.get('air_quality', {})
air_quality_index = air_quality.get('us-epa-index', 'N/A')

# Print extracted data
print("\n✅ Extracted Weather Data:")
print(f"🌡 Temperature: {temperature}°C")
print(f"💨 Wind Speed: {wind_speed} m/s")
print(f"💧 Humidity: {humidity}%")
print(f"🌫 Dew Point: {dew_point}°C")
print(f"⚖ Pressure: {pressure} Pa")
print(f"☀ UV Index: {uv_index}")
print(f"👁 Visibility: {visibility} meters")
print(f"🌙 Moon Phase: {moon_phase}")
print(f"🌍 Air Quality Index (EPA): {air_quality_index}")

# Fetch historical weather data
start_date = "2020-01-01"
historical_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,cloud_cover_mean&timezone=Asia/Manila"

try:
    response = requests.get(historical_url, timeout=15)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching historical weather data: {e}")
    exit()

if "daily" in data:
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temperature_max": data["daily"]["temperature_2m_max"],
        "temperature_min": data["daily"]["temperature_2m_min"],
        "rainfall": data["daily"]["precipitation_sum"],
        "wind_speed": data["daily"]["wind_speed_10m_max"],
        "cloud_cover": data["daily"]["cloud_cover_mean"]
    })

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.fillna(method='ffill', inplace=True)

    df['month'] = df.index.month
    df['day'] = df.index.day

    # Scale the data
    scaler = StandardScaler()
    features = ['temperature_max', 'temperature_min', 'rainfall', 'wind_speed', 'cloud_cover']
    df[features] = scaler.fit_transform(df[features])

    # Prepare dataset
    X = df[features].values
    y = df[features].shift(-1).dropna().values
    X = X[:-1]  # Ensure same shape

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Reshape for LSTM
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    # Define LSTM model
    model = Sequential([
        LSTM(64, return_sequences=True, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
        LSTM(32, activation='relu'),
        Dense(5)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # Train model
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

    # Evaluate model
    loss, mae = model.evaluate(X_test, y_test)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    # Calculate additional accuracy metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100  # Convert to percentage

    # Print results
    print(f"\n📉 Test loss (MSE): {loss:.4f}")
    print(f"📏 Mean Absolute Error (MAE): {mae:.4f}")
    print(f"📊 R² Score: {r2:.4f}")
    print(f"📈 RMSE (Root Mean Squared Error): {rmse:.4f}")
    print(f"🎯 MAPE (Mean Absolute Percentage Error): {mape:.2f}%")

    # Generate 30-day forecast
    forecast = []
    last_data = X[-1].reshape(1, 1, X.shape[1])
    for _ in range(30):
        predicted = model.predict(last_data)
        forecast.append(predicted[0])
        last_data = np.roll(last_data, -1, axis=2)
        last_data[0, 0, -1] = predicted[0][-1]

    forecast = np.array(forecast)
    forecast_values = scaler.inverse_transform(forecast)

    forecast_df = pd.DataFrame({
        'date': pd.date_range(start=end_date, periods=30, freq='D'),
        'temperature_max': forecast_values[:, 0],
        'temperature_min': forecast_values[:, 1],
        'rainfall': forecast_values[:, 2],
        'wind_speed': forecast_values[:, 3],
        'cloud_cover': forecast_values[:, 4]
    })

    forecast_df.to_csv('forecasted_weather_data.csv', index=False)
    print("\n✅ Weather forecast saved to 'forecasted_weather_data.csv'!")
else:
    print("❌ API did not return expected weather data.")
