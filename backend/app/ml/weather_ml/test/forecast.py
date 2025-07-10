# nagana kaso yung value nya ay super duper unrealistic

# import requests
# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score, mean_squared_error
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# from datetime import datetime
# from dotenv import load_dotenv
# import os

# # Load API key from environment variable
# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")  # Make sure to set this in your .env file
# LOCATION = "Parang, Calapan City, Oriental Mindoro"

# # Function to fetch current weather data from WeatherAPI
# def fetch_current_weather():
#     current_weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}&aqi=yes"
#     try:
#         response = requests.get(current_weather_url, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching current weather data: {e}")
#         return None

# # Load historical weather data
# df = pd.read_csv('dataset.csv')
# df['date'] = pd.to_datetime(df['date'])
# df.set_index('date', inplace=True)

# # Define features to use for training
# features = ['temperature_max', 'temperature_min', 'rainfall', 'precipitation_hours', 'snowfall', 
#             'wind_speed', 'cloud_cover', 'humidity', 'pressure']

# # Drop NaN values to ensure clean data
# df.dropna(inplace=True)

# # Normalize the features
# scaler = StandardScaler()
# df[features] = scaler.fit_transform(df[features])

# # Prepare dataset for LSTM
# X = df[features].values[:-1]  # Exclude last row
# y = df[features].shift(-1).dropna().values  # Shift target and remove NaNs

# # Ensure X and y have the same number of samples
# if X.shape[0] != y.shape[0]:
#     min_samples = min(X.shape[0], y.shape[0])
#     X, y = X[:min_samples], y[:min_samples]

# # Final shape check
# assert X.shape[0] == y.shape[0], f"X and y must have the same number of samples: X={X.shape[0]}, y={y.shape[0]}"

# # Split into train and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# # Reshape for LSTM input (samples, timesteps, features)
# X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
# X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# # Define the LSTM model
# model = Sequential([
#     LSTM(64, return_sequences=True, activation='relu', input_shape=(1, X_train.shape[2])),
#     LSTM(32, activation='relu'),
#     Dense(len(features))  # Predicting all 9 weather features
# ])

# model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# # Train the model
# model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

# # Evaluate the model
# loss, mae = model.evaluate(X_test, y_test)
# y_pred = model.predict(X_test)

# # Fix NaN issues in y_pred
# y_pred = np.nan_to_num(y_pred)  # Convert NaNs to 0 to avoid errors

# # Calculate evaluation metrics
# r2 = r2_score(y_test, y_pred)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# print(f"✅ Model Evaluation Results:")
# print(f"Test Loss (MSE): {loss:.4f}")
# print(f"Mean Absolute Error (MAE): {mae:.4f}")
# print(f"R² Score: {r2:.4f}")
# print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

# # Fetch current weather data
# current_weather = fetch_current_weather()

# if current_weather:
#     current_conditions = current_weather.get('current', {})
#     temperature = current_conditions.get('temp_c', 0)
#     wind_speed = current_conditions.get('wind_kph', 0) * 0.277778  # Convert km/h to m/s
#     humidity = current_conditions.get('humidity', 0)
#     pressure = current_conditions.get('pressure_mb', 0) * 100  # Convert mb to Pa
#     cloud_cover = current_conditions.get('cloud', 0)

#     # Prepare current weather data for prediction
#     current_data = np.array([[temperature, temperature, 0, 0, 0, wind_speed, cloud_cover, humidity, pressure]])
    
#     # Normalize current data
#     current_data = scaler.transform(current_data)
#     current_data = current_data.reshape((1, 1, current_data.shape[1]))  # Reshape for LSTM

#     # Forecast for the next 30 days
#     forecast = []
#     for day in range(30):
#         predicted = model.predict(current_data)
#         predicted = np.nan_to_num(predicted)  # Ensure no NaN values in predictions
#         forecast.append(predicted[0])

#         # Update input for next day
#         current_data = predicted.reshape((1, 1, predicted.shape[1]))

#     # Convert forecast back to original scale
#     forecast_values = scaler.inverse_transform(forecast)

#     # Save forecast results
#     forecast_df = pd.DataFrame(forecast_values, columns=features)
#     forecast_df['date'] = pd.date_range(start=datetime.today(), periods=30, freq='D')

#     forecast_df.to_csv('forecasted_weather_1_month.csv', index=False)
#     print(f"✅ Forecast for the next 30 days saved to 'forecasted_weather_1_month.csv'!")

# else:
#     print("❌ Could not retrieve current weather data.")


#=================================#
# ito ay para sa train ng model para sa forecasting, 

# import numpy as np
# import pandas as pd
# from sklearn.model_selection import TimeSeriesSplit
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
# from tensorflow import keras
# from tensorflow.keras import layers, callbacks, Model
# from tensorflow.keras.optimizers import Adam
# import matplotlib.pyplot as plt
# import joblib

# # Load and preprocess data
# def load_data(filepath):
#     df = pd.read_csv(filepath, parse_dates=['date'])
#     df.sort_values('date', inplace=True)
#     return df

# # Feature engineering
# def engineer_features(df, target_cols, n_lags=3):
#     # Time features
#     df['day_of_year'] = df['date'].dt.dayofyear
#     df['month'] = df['date'].dt.month
#     df['year'] = df['date'].dt.year
    
#     # Cyclical encoding
#     df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
#     df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
#     # Lag features for all targets
#     for col in target_cols:
#         for lag in range(1, n_lags+1):
#             df[f'{col}_lag_{lag}'] = df[col].shift(lag)
    
#     # Drop initial NaN rows from lag features
#     df.dropna(inplace=True)
#     return df

# # Main function
# def main():
#     # Configuration
#     TARGET_COLS = ['temperature_max', 'rainfall', 'precipitation_hours', 'snowfall' , 'wind_speed', 'cloud_cover', 'humidity', 'pressure']  # Update with your columns
#     MODEL_SAVE_PATH = 'weather_forecaster.h5'
#     SCALER_SAVE_PATH = 'scalers.pkl'
    
#     # Load data
#     df = load_data("dataset.csv")
    
#     # Feature engineering
#     df = engineer_features(df, TARGET_COLS)
    
#     # Split features and targets
#     X = df.drop(columns=['date'] + TARGET_COLS)
#     y = df[TARGET_COLS]
    
#     # Time-based split
#     split_idx = int(len(df) * 0.8)
#     X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
#     y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
#     # Scaling
#     scaler_X = MinMaxScaler()
#     X_train_scaled = scaler_X.fit_transform(X_train)
#     X_test_scaled = scaler_X.transform(X_test)
    
#     scaler_y = MinMaxScaler()
#     y_train_scaled = scaler_y.fit_transform(y_train)
#     y_test_scaled = scaler_y.transform(y_test)
    
#     # Save scalers
#     joblib.dump({'X': scaler_X, 'y': scaler_y}, SCALER_SAVE_PATH)
    
#     # Build model
#     inputs = layers.Input(shape=(X_train_scaled.shape[1],))
#     x = layers.Dense(256, activation='relu')(inputs)
#     x = layers.BatchNormalization()(x)
#     x = layers.Dropout(0.3)(x)
#     x = layers.Dense(128, activation='relu')(x)
#     x = layers.Dropout(0.2)(x)
#     x = layers.Dense(64, activation='relu')(x)
#     outputs = layers.Dense(len(TARGET_COLS), activation='linear')(x)
    
#     model = Model(inputs=inputs, outputs=outputs)
    
#     # Compile
#     model.compile(
#         optimizer=Adam(learning_rate=0.001),
#         loss='mse',
#         metrics=['mae']
#     )
    
#     # Callbacks
#     callbacks_list = [
#         callbacks.EarlyStopping(patience=15, restore_best_weights=True),
#         callbacks.ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True)
#     ]
    
#     # Train
#     history = model.fit(
#         X_train_scaled, y_train_scaled,
#         epochs=200,
#         batch_size=32,
#         validation_split=0.1,
#         callbacks=callbacks_list,
#         verbose=1
#     )
    
#     # Save final model
#     model.save(MODEL_SAVE_PATH)
    
#     # Evaluate
#     y_pred_scaled = model.predict(X_test_scaled)
#     y_pred = scaler_y.inverse_transform(y_pred_scaled)
#     y_test_orig = scaler_y.inverse_transform(y_test_scaled)
    
#     # Calculate metrics for each target
#     metrics = {}
#     for i, col in enumerate(TARGET_COLS):
#         metrics[col] = {
#             'MAE': mean_absolute_error(y_test_orig[:,i], y_pred[:,i]),
#             'RMSE': np.sqrt(mean_squared_error(y_test_orig[:,i], y_pred[:,i])),
#             'R²': r2_score(y_test_orig[:,i], y_pred[:,i])
#         }
    
#     # Print metrics
#     print("\n✅ Model Evaluation Results:")
#     for col, vals in metrics.items():
#         print(f"\n📊 {col}:")
#         print(f"MAE: {vals['MAE']:.4f}")
#         print(f"RMSE: {vals['RMSE']:.4f}")
#         print(f"R²: {vals['R²']:.4f}")
    
#     # Plot results
#     plt.figure(figsize=(15, 4*len(TARGET_COLS)))
#     for i, col in enumerate(TARGET_COLS):
#         plt.subplot(len(TARGET_COLS), 1, i+1)
#         plt.plot(y_test_orig[:,i], label='Actual')
#         plt.plot(y_pred[:,i], label='Predicted', alpha=0.7)
#         plt.title(f'{col} Forecast')
#         plt.legend()
#     plt.tight_layout()
#     plt.show()

# if __name__ == "__main__":
#     main()



#===========================================#
# ito ay may error na malupet


# import requests
# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score, mean_squared_error
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load API key from environment variable
# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")
# LOCATION = "Parang, Calapan City, Oriental Mindoro"
# LATITUDE = 13.3895
# LONGITUDE = 121.2312

# # Set random seeds for reproducibility
# np.random.seed(42)
# tf.random.set_seed(42)

# # Function to fetch current weather data from WeatherAPI
# def fetch_current_weather():
#     current_weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}&aqi=yes"
#     try:
#         response = requests.get(current_weather_url, timeout=10)
#         response.raise_for_status()
#         current_weather = response.json()
#         return current_weather
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching current weather data: {e}")
#         return None

# # Load historical weather data
# print("📊 Loading historical weather data...")
# df = pd.read_csv('historical_weather_data.csv')
# df['date'] = pd.to_datetime(df['date'])
# print(f"Dataset shape: {df.shape}")
# print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# # Data Preprocessing
# features = ['temperature_max', 'temperature_min', 'precipitation', 'wind_speed', 'cloud_cover']
# print(f"Using features: {features}")

# # Set min and max constraints for each feature (based on Calapan City climate)
# feature_constraints = {
#     'temperature_max': (24, 35),  # °C (typical range for Calapan City)
#     'temperature_min': (20, 28),  # °C
#     'precipitation': (0, 25),     # mm
#     'wind_speed': (0, 15),        # m/s
#     'cloud_cover': (0, 100)       # %
# }

# # Check and handle missing values
# missing_values = df[features].isna().sum()
# if missing_values.sum() > 0:
#     print(f"Warning: Found missing values: {missing_values}")
#     df[features] = df[features].fillna(df[features].median())

# # Use MinMaxScaler instead of StandardScaler for better bounds control
# scalers = {}
# df_scaled = pd.DataFrame(index=df.index)

# # Scale each feature individually to maintain better control
# for feature in features:
#     scaler = MinMaxScaler(feature_range=(0, 1))
#     df_scaled[feature] = scaler.fit_transform(df[[feature]])
#     scalers[feature] = scaler

# # Add month and day features to capture seasonality
# df['month'] = df['date'].dt.month
# df['day'] = df['date'].dt.day
# df_scaled['month'] = df['month'] / 12  # Scale month to [0,1]
# df_scaled['day'] = df['day'] / 31      # Scale day to [0,1]

# # Create sequences for the LSTM model
# def create_sequences(data, seq_length):
#     X, y = [], []
#     for i in range(len(data) - seq_length):
#         X.append(data[i:i+seq_length])
#         y.append(data[i+seq_length, :len(features)])  # Only predict the weather features
#     return np.array(X), np.array(y)

# # Use 14 days of history to predict the next day
# SEQ_LENGTH = 14

# # Create sequences from scaled data including month/day features
# X, y = create_sequences(df_scaled.values, SEQ_LENGTH)

# # Train-validation-test split (preserve time ordering)
# train_size = int(len(X) * 0.7)
# val_size = int(len(X) * 0.15)

# X_train, y_train = X[:train_size], y[:train_size]
# X_val, y_val = X[train_size:train_size+val_size], y[train_size:train_size+val_size]
# X_test, y_test = X[train_size+val_size:], y[train_size+val_size:]

# print(f"Training set: {X_train.shape}, Validation set: {X_val.shape}, Test set: {X_test.shape}")

# # Build a more sophisticated LSTM model
# model = Sequential([
#     # First LSTM layer with dropout
#     LSTM(128, activation='tanh', return_sequences=True, 
#          input_shape=(SEQ_LENGTH, X_train.shape[2])),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     # Second LSTM layer with dropout
#     LSTM(64, activation='tanh'),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     # Dense layers
#     Dense(32, activation='relu'),
#     BatchNormalization(),
#     Dropout(0.2),
    
#     # Output layer for the 5 features
#     Dense(len(features), activation='sigmoid')  # Sigmoid keeps values in [0,1] range
# ])

# # Compile with reduced learning rate and appropriate metrics
# model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#     loss='mse',
#     metrics=['mae']
# )

# # Add callbacks for better training
# callbacks = [
#     EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
#     ModelCheckpoint('best_weather_model.h5', save_best_only=True, monitor='val_loss')
# ]

# # Train the model
# print("\n🧠 Training the model...")
# history = model.fit(
#     X_train, y_train,
#     validation_data=(X_val, y_val),
#     epochs=100,
#     batch_size=32,
#     callbacks=callbacks,
#     verbose=1
# )

# # Evaluate on test data
# print("\n📝 Evaluating model performance...")
# test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
# y_pred = model.predict(X_test)

# # Calculate metrics
# r2 = r2_score(y_test, y_pred)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# print(f"Test Loss (MSE): {test_loss:.4f}")
# print(f"Mean Absolute Error (MAE): {test_mae:.4f}")
# print(f"R² Score: {r2:.4f}")
# print(f"RMSE: {rmse:.4f}")

# # Fetch current weather data
# print("\n🌤️ Fetching current weather data...")
# current_weather = fetch_current_weather()

# # Define a function for more controlled, realistic forecasting
# def generate_realistic_forecast(model, last_known_sequence, days=30):
#     """Generate a realistic forecast with constraints to prevent unrealistic values."""
    
#     # Make a copy of the last known sequence to avoid modifying the original
#     current_sequence = last_known_sequence.copy()
    
#     forecasts = []
    
#     # Get the last date from the dataframe
#     last_date = df['date'].iloc[-1]  # Use df['date'] instead of df.index
    
#     # Forecast one day at a time
#     for i in range(days):
#         # Predict the next day (keep only weather features, not month/day)
#         pred = model.predict(np.array([current_sequence]), verbose=0)[0]
#         forecasts.append(pred)
        
#         # Prepare for next day prediction
#         next_day_date = last_date + timedelta(days=i+1)
        
#         # Update month and day for the next prediction
#         next_month = next_day_date.month / 12  # Scaled month
#         next_day = next_day_date.day / 31      # Scaled day
        
#         # Create next sequence by removing the first day and adding the new prediction
#         next_sequence = np.roll(current_sequence, -1, axis=0)
        
#         # Add the weather features to the sequence
#         next_sequence[-1, :len(features)] = pred
        
#         # Add month and day features to capture seasonality
#         next_sequence[-1, len(features)] = next_month  # Add scaled month
#         next_sequence[-1, len(features)+1] = next_day  # Add scaled day
        
#         # Update current sequence for next iteration
#         current_sequence = next_sequence
    
#     return np.array(forecasts)

# if current_weather:
#     # Extract current weather data
#     current_conditions = current_weather.get('current', {})
    
#     # Get the latest date from historical data
#     last_date = df['date'].iloc[-1]  # Changed from df.index[-1] to df['date'].iloc[-1]
    
#     # Get today's date
#     today = datetime.now()
    
#     # Create a sequence of the last SEQ_LENGTH days
#     last_sequence = df_scaled.iloc[-SEQ_LENGTH:].values
    
#     # Generate forecast
#     print(f"\n🔮 Generating forecast for the next 30 days starting from {today.strftime('%Y-%m-%d')}...")
#     forecast_scaled = generate_realistic_forecast(model, last_sequence, days=30)
    
#     # Prepare dates for forecast
#     forecast_dates = [today + timedelta(days=i) for i in range(30)]
    
#     # Create a DataFrame for the forecast
#     forecast_df = pd.DataFrame()
    
#     # Inverse transform each feature
#     for i, feature in enumerate(features):
#         forecast_values = forecast_scaled[:, i].reshape(-1, 1)
#         forecast_df[feature] = scalers[feature].inverse_transform(forecast_values).flatten()
    
#     # Add dates
#     forecast_df['date'] = forecast_dates
    
#     # Apply constraints to ensure realistic values (using feature_constraints)
#     for feature, (min_val, max_val) in feature_constraints.items():
#         forecast_df[feature] = forecast_df[feature].clip(min_val, max_val)
    
#     # Make sure min temperature is always less than max temperature
#     temp_diff = forecast_df['temperature_max'] - forecast_df['temperature_min']
    
#     # Where min > max or diff is too small, adjust both
#     for i in range(len(forecast_df)):
#         if temp_diff[i] < 2:  # Ensure at least 2°C difference
#             avg_temp = (forecast_df.loc[i, 'temperature_max'] + forecast_df.loc[i, 'temperature_min']) / 2
#             forecast_df.loc[i, 'temperature_max'] = min(avg_temp + 2, feature_constraints['temperature_max'][1])
#             forecast_df.loc[i, 'temperature_min'] = max(avg_temp - 2, feature_constraints['temperature_min'][0])
    
#     # Print forecast summary
#     print("\n📊 Forecast Summary (Next 7 days):")
#     for i in range(min(7, len(forecast_df))):
#         day_forecast = forecast_df.iloc[i]
#         print(f"📅 {day_forecast['date'].strftime('%Y-%m-%d')}: "
#               f"Max: {day_forecast['temperature_max']:.1f}°C, "
#               f"Min: {day_forecast['temperature_min']:.1f}°C, "
#               f"Precip: {day_forecast['precipitation']:.1f}mm, "
#               f"Wind: {day_forecast['wind_speed']:.1f}m/s, "
#               f"Cloud: {day_forecast['cloud_cover']:.0f}%")
    
#     # Save forecast to CSV
#     output_file = 'forecasted_weather_1_month.csv'
#     forecast_df.to_csv(output_file, index=False)
#     print(f"\n✅ Complete 30-day forecast saved to '{output_file}'!")
    
# else:
#     print("❌ Could not retrieve current weather data.")

#============================================================3
# may error din itong code na ito

# import requests
# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score, mean_squared_error
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load API key from environment variable
# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")
# LOCATION = "Parang, Calapan City, Oriental Mindoro"
# LATITUDE = 13.3895
# LONGITUDE = 121.2312

# # Set random seeds for reproducibility
# np.random.seed(42)
# tf.random.set_seed(42)

# # Function to fetch current weather data from WeatherAPI
# def fetch_current_weather():
#     current_weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}&aqi=yes"
#     try:
#         response = requests.get(current_weather_url, timeout=10)
#         response.raise_for_status()
#         current_weather = response.json()
#         return current_weather
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching current weather data: {e}")
#         return None

# # Load historical weather data
# print("📊 Loading historical weather data...")
# df = pd.read_csv('dataset.csv')
# df['date'] = pd.to_datetime(df['date'])
# print(f"Dataset shape: {df.shape}")
# print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# # Data Preprocessing
# features = ['temperature_max', 'temperature_min', 'precipitation', 'wind_speed', 'cloud_cover']
# print(f"Using features: {features}")

# # Set min and max constraints for each feature (based on Calapan City climate)
# feature_constraints = {
#     'temperature_max': (24, 35),  # °C (typical range for Calapan City)
#     'temperature_min': (20, 28),  # °C
#     'precipitation': (0, 25),     # mm
#     'wind_speed': (0, 15),        # m/s
#     'cloud_cover': (0, 100)       # %
# }

# # Check and handle missing values
# missing_values = df[features].isna().sum()
# if missing_values.sum() > 0:
#     print(f"Warning: Found missing values: {missing_values}")
#     df[features] = df[features].fillna(df[features].median())

# # Use MinMaxScaler instead of StandardScaler for better bounds control
# scalers = {}
# df_scaled = pd.DataFrame(index=df.index)

# # Scale each feature individually to maintain better control
# for feature in features:
#     scaler = MinMaxScaler(feature_range=(0, 1))
#     df_scaled[feature] = scaler.fit_transform(df[[feature]])
#     scalers[feature] = scaler

# # Add month and day features to capture seasonality
# df['month'] = df['date'].dt.month
# df['day'] = df['date'].dt.day
# df_scaled['month'] = df['month'] / 12  # Scale month to [0,1]
# df_scaled['day'] = df['day'] / 31      # Scale day to [0,1]

# # Create sequences for the LSTM model
# def create_sequences(data, seq_length):
#     X, y = [], []
#     for i in range(len(data) - seq_length):
#         X.append(data[i:i+seq_length])
#         y.append(data[i+seq_length, :len(features)])  # Only predict the weather features
#     return np.array(X), np.array(y)

# # Use 14 days of history to predict the next day
# SEQ_LENGTH = 14

# # Create sequences from scaled data including month/day features
# X, y = create_sequences(df_scaled.values, SEQ_LENGTH)

# # Train-validation-test split (preserve time ordering)
# train_size = int(len(X) * 0.7)
# val_size = int(len(X) * 0.15)

# X_train, y_train = X[:train_size], y[:train_size]
# X_val, y_val = X[train_size:train_size+val_size], y[train_size:train_size+val_size]
# X_test, y_test = X[train_size+val_size:], y[train_size+val_size:]

# print(f"Training set: {X_train.shape}, Validation set: {X_val.shape}, Test set: {X_test.shape}")

# # Build a more sophisticated LSTM model
# model = Sequential([
#     # First LSTM layer with dropout
#     LSTM(128, activation='tanh', return_sequences=True, 
#          input_shape=(SEQ_LENGTH, X_train.shape[2])),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     # Second LSTM layer with dropout
#     LSTM(64, activation='tanh'),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     # Dense layers
#     Dense(32, activation='relu'),
#     BatchNormalization(),
#     Dropout(0.2),
    
#     # Output layer for the 5 features
#     Dense(len(features), activation='sigmoid')  # Sigmoid keeps values in [0,1] range
# ])

# # Compile with reduced learning rate and appropriate metrics
# model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#     loss='mse',
#     metrics=['mae']
# )

# # Add callbacks for better training
# callbacks = [
#     EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
#     ModelCheckpoint('best_weather_model.h5', save_best_only=True, monitor='val_loss')
# ]

# # Train the model
# print("\n🧠 Training the model...")
# history = model.fit(
#     X_train, y_train,
#     validation_data=(X_val, y_val),
#     epochs=100,
#     batch_size=32,
#     callbacks=callbacks,
#     verbose=1
# )

# # Evaluate on test data
# print("\n📝 Evaluating model performance...")
# test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
# y_pred = model.predict(X_test)

# # Calculate metrics
# r2 = r2_score(y_test, y_pred)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# print(f"Test Loss (MSE): {test_loss:.4f}")
# print(f"Mean Absolute Error (MAE): {test_mae:.4f}")
# print(f"R² Score: {r2:.4f}")
# print(f"RMSE: {rmse:.4f}")

# # Fetch current weather data
# print("\n🌤️ Fetching current weather data...")
# current_weather = fetch_current_weather()

# # Define a function for more controlled, realistic forecasting
# def generate_realistic_forecast(model, last_known_sequence, days=30):
#     """Generate a realistic forecast with constraints to prevent unrealistic values."""
    
#     # Make a copy of the last known sequence to avoid modifying the original
#     current_sequence = last_known_sequence.copy()
    
#     forecasts = []
    
#     # Get the last date from the dataframe
#     last_date = df['date'].iloc[-1]  # Use df['date'] instead of df.index
    
#     # Forecast one day at a time
#     for i in range(days):
#         # Predict the next day (keep only weather features, not month/day)
#         pred = model.predict(np.array([current_sequence]), verbose=0)[0]
#         forecasts.append(pred)
        
#         # Prepare for next day prediction
#         next_day_date = last_date + timedelta(days=i+1)
        
#         # Update month and day for the next prediction
#         next_month = next_day_date.month / 12  # Scaled month
#         next_day = next_day_date.day / 31      # Scaled day
        
#         # Create next sequence by removing the first day and adding the new prediction
#         next_sequence = np.roll(current_sequence, -1, axis=0)
        
#         # Add the weather features to the sequence
#         next_sequence[-1, :len(features)] = pred
        
#         # Add month and day features to capture seasonality
#         next_sequence[-1, len(features)] = next_month  # Add scaled month
#         next_sequence[-1, len(features)+1] = next_day  # Add scaled day
        
#         # Update current sequence for next iteration
#         current_sequence = next_sequence
    
#     return np.array(forecasts)

# if current_weather:
#     # Extract current weather data
#     current_conditions = current_weather.get('current', {})
    
#     # Get the latest date from historical data
#     last_date = df['date'].iloc[-1]  # Changed from df.index[-1] to df['date'].iloc[-1]
    
#     # Get today's date
#     today = datetime.now()
    
#     # Create a sequence of the last SEQ_LENGTH days
#     last_sequence = df_scaled.iloc[-SEQ_LENGTH:].values
    
#     # Generate forecast
#     print(f"\n🔮 Generating forecast for the next 30 days starting from {today.strftime('%Y-%m-%d')}...")
#     forecast_scaled = generate_realistic_forecast(model, last_sequence, days=30)
    
#     # Prepare dates for forecast
#     forecast_dates = [today + timedelta(days=i) for i in range(30)]
    
#     # Create a DataFrame for the forecast
#     forecast_df = pd.DataFrame()
    
#     # Inverse transform each feature
#     for i, feature in enumerate(features):
#         forecast_values = forecast_scaled[:, i].reshape(-1, 1)
#         forecast_df[feature] = scalers[feature].inverse_transform(forecast_values).flatten()
    
#     # Add dates
#     forecast_df['date'] = forecast_dates
    
#     # Apply constraints to ensure realistic values (using feature_constraints)
#     for feature, (min_val, max_val) in feature_constraints.items():
#         forecast_df[feature] = forecast_df[feature].clip(min_val, max_val)
    
#     # Make sure min temperature is always less than max temperature
#     temp_diff = forecast_df['temperature_max'] - forecast_df['temperature_min']
    
#     # Where min > max or diff is too small, adjust both
#     for i in range(len(forecast_df)):
#         if temp_diff[i] < 2:  # Ensure at least 2°C difference
#             avg_temp = (forecast_df.loc[i, 'temperature_max'] + forecast_df.loc[i, 'temperature_min']) / 2
#             forecast_df.loc[i, 'temperature_max'] = min(avg_temp + 2, feature_constraints['temperature_max'][1])
#             forecast_df.loc[i, 'temperature_min'] = max(avg_temp - 2, feature_constraints['temperature_min'][0])
    
#     # Print forecast summary
#     print("\n📊 Forecast Summary (Next 7 days):")
#     for i in range(min(7, len(forecast_df))):
#         day_forecast = forecast_df.iloc[i]
#         print(f"📅 {day_forecast['date'].strftime('%Y-%m-%d')}: "
#               f"Max: {day_forecast['temperature_max']:.1f}°C, "
#               f"Min: {day_forecast['temperature_min']:.1f}°C, "
#               f"Precip: {day_forecast['precipitation']:.1f}mm, "
#               f"Wind: {day_forecast['wind_speed']:.1f}m/s, "
#               f"Cloud: {day_forecast['cloud_cover']:.0f}%")
    
#     # Save forecast to CSV
#     output_file = 'forecasted_weather_1_month.csv'
#     forecast_df.to_csv(output_file, index=False)
#     print(f"\n✅ Complete 30-day forecast saved to '{output_file}'!")
    
# else:
#     print("❌ Could not retrieve current weather data.")

#======================================================#
# nagerror din ito

# import requests
# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score, mean_squared_error
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import os

# # Load API key from environment variable
# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")
# LOCATION = "Parang, Calapan City, Oriental Mindoro"

# # Set random seeds for reproducibility
# np.random.seed(42)
# tf.random.set_seed(42)

# # Function to fetch current weather data
# def fetch_current_weather():
#     current_weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}&aqi=yes"
#     try:
#         response = requests.get(current_weather_url, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching current weather data: {e}")
#         return None

# # Load historical weather data
# print("📊 Loading historical weather data...")
# df = pd.read_csv('dataset.csv')
# df['date'] = pd.to_datetime(df['date'])

# # Features to be used for training
# weather_features = ['temperature_max', 'temperature_min', 'precipitation', 'wind_speed', 'cloud_cover']
# print(f"Using features: {weather_features}")

# # Check and fill missing values
# df[weather_features] = df[weather_features].fillna(df[weather_features].median())

# # Define feature constraints (ensuring realistic values)
# feature_constraints = {
#     'temperature_max': (24, 35),
#     'temperature_min': (20, 28),
#     'precipitation': (0, 25),
#     'wind_speed': (0, 15),
#     'cloud_cover': (0, 100)
# }

# # Normalize data using MinMaxScaler
# scaler_weather = MinMaxScaler(feature_range=(0, 1))
# df_scaled = pd.DataFrame(scaler_weather.fit_transform(df[weather_features]), columns=weather_features, index=df.index)

# # Add time-based features
# df['month'] = df['date'].dt.month / 12
# df['day'] = df['date'].dt.day / 31
# df_scaled['month'] = df['month']
# df_scaled['day'] = df['day']

# # Function to create sequences
# def create_sequences(data, seq_length):
#     X, y = [], []
#     for i in range(len(data) - seq_length):
#         X.append(data[i:i+seq_length])
#         y.append(data[i+seq_length, :len(weather_features)])
#     return np.array(X), np.array(y)

# # Sequence length for LSTM (14 days)
# SEQ_LENGTH = 14

# # Create sequences from scaled data
# X, y = create_sequences(df_scaled.values, SEQ_LENGTH)

# # Train-validation-test split (time-ordered)
# train_size = int(len(X) * 0.7)
# val_size = int(len(X) * 0.15)

# X_train, y_train = X[:train_size], y[:train_size]
# X_val, y_val = X[train_size:train_size+val_size], y[train_size:train_size+val_size]
# X_test, y_test = X[train_size+val_size:], y[train_size+val_size:]

# print(f"Training set: {X_train.shape}, Validation set: {X_val.shape}, Test set: {X_test.shape}")

# # Build LSTM model
# model = Sequential([
#     LSTM(128, activation='tanh', return_sequences=True, input_shape=(SEQ_LENGTH, X_train.shape[2])),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     LSTM(64, activation='tanh'),
#     BatchNormalization(),
#     Dropout(0.3),
    
#     Dense(32, activation='relu'),
#     BatchNormalization(),
#     Dropout(0.2),
    
#     Dense(len(weather_features), activation='sigmoid')
# ])

# # Compile model
# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

# # Callbacks for early stopping and model checkpointing
# callbacks = [
#     EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
#     ModelCheckpoint('best_weather_model.h5', save_best_only=True, monitor='val_loss')
# ]

# # Train the model
# print("\n🧠 Training the model...")
# history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100, batch_size=32, callbacks=callbacks, verbose=1)

# # Evaluate the model
# print("\n📝 Evaluating model performance...")
# test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
# y_pred = model.predict(X_test)

# # Calculate metrics
# r2 = r2_score(y_test, y_pred)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# print(f"Test Loss (MSE): {test_loss:.4f}")
# print(f"Mean Absolute Error (MAE): {test_mae:.4f}")
# print(f"R² Score: {r2:.4f}")
# print(f"RMSE: {rmse:.4f}")

# # Forecast function
# def generate_realistic_forecast(model, last_known_sequence, days=30):
#     current_sequence = last_known_sequence.copy()
#     forecasts = []
#     last_date = df['date'].iloc[-1]
    
#     for i in range(days):
#         pred = model.predict(np.array([current_sequence]), verbose=0)[0]
#         forecasts.append(pred)
        
#         next_day_date = last_date + timedelta(days=i+1)
#         next_month = next_day_date.month / 12
#         next_day = next_day_date.day / 31
        
#         next_sequence = np.roll(current_sequence, -1, axis=0)
#         next_sequence[-1, :len(weather_features)] = pred
#         next_sequence[-1, len(weather_features)] = next_month
#         next_sequence[-1, len(weather_features)+1] = next_day
        
#         current_sequence = next_sequence
    
#     return np.array(forecasts)

# # Fetch current weather
# print("\n🌤️ Fetching current weather data...")
# current_weather = fetch_current_weather()

# if current_weather:
#     last_sequence = df_scaled.iloc[-SEQ_LENGTH:].values
#     print("\n🔮 Generating forecast for the next 30 days...")
#     forecast_scaled = generate_realistic_forecast(model, last_sequence, days=30)
    
#     # Convert forecasted values back to original scale
#     forecast_df = pd.DataFrame(
#         scaler_weather.inverse_transform(forecast_scaled), 
#         columns=weather_features
#     )
    
#     # Generate forecast dates
#     forecast_df['date'] = [datetime.now() + timedelta(days=i) for i in range(30)]
    
#     # Apply feature constraints
#     for feature, (min_val, max_val) in feature_constraints.items():
#         forecast_df[feature] = forecast_df[feature].clip(min_val, max_val)
    
#     # Ensure min temperature is always lower than max temperature
#     for i in range(len(forecast_df)):
#         if forecast_df.loc[i, 'temperature_max'] < forecast_df.loc[i, 'temperature_min']:
#             avg_temp = (forecast_df.loc[i, 'temperature_max'] + forecast_df.loc[i, 'temperature_min']) / 2
#             forecast_df.loc[i, 'temperature_max'] = avg_temp + 1
#             forecast_df.loc[i, 'temperature_min'] = avg_temp - 1
    
#     # Save forecast to CSV
#     output_file = 'forecasted_weather_1_month.csv'
#     forecast_df.to_csv(output_file, index=False)
#     print(f"\n✅ Forecast saved to '{output_file}'!")
# else:
#     print("❌ Could not retrieve current weather data.")

#=========================================#
# ITO YUNG NAGANA NA GALING API KASO HANGGANG 3 DAYS AHEAD LANG YUNG FOREACASTING


# import requests
# import pandas as pd
# from dotenv import load_dotenv
# import os

# # Load API key from environment variable
# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")

# LOCATION = "13.3895,121.2312"  # Parang, Calapan City coordinates
# DAYS = 30

# def get_weather_forecast():
#     url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days={DAYS}&aqi=no&alerts=no"
    
#     response = requests.get(url)
#     data = response.json()
    
#     if "error" in data:
#         raise ValueError(f"API Error: {data['error']['message']}")
    
#     forecast_data = []
#     for day in data["forecast"]["forecastday"]:
#         # Get first hour data for pressure and cloud cover
#         first_hour = day["hour"][0]
        
#         forecast_data.append({
#             "date": day["date"],
#             "temperature_c": day["day"]["avgtemp_c"],
#             "temperature_f": day["day"]["avgtemp_f"],
#             "humidity": day["day"]["avghumidity"],
#             "wind_speed_kph": day["day"]["maxwind_kph"],
#             "pressure_hpa": first_hour["pressure_mb"] * 1.0,  # Convert mb to hPa (1:1 ratio)
#             "cloud_cover_percent": first_hour["cloud"],
#             "weather_condition": day["day"]["condition"]["text"],
#             "rain_mm": day["day"]["totalprecip_mm"]
#         })
    
#     return pd.DataFrame(forecast_data)

# # Execute and save
# try:
#     df = get_weather_forecast()
#     df.to_csv("weather_forecast_30days.csv", index=False)
#     print("✅ Forecast saved successfully!")
#     print(df.head())
# except Exception as e:
#     print(f"❌ Error: {str(e)}")

#===================================================#
# ITO AY NAGANA PERO HINDI KO ALAM KUNG TAMA BA ANG NAGING FORECASTING


# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# import requests
# import json
# import matplotlib.pyplot as plt
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# import os
# from dotenv import load_dotenv

# # Function to load historical weather data
# def load_historical_data(file_path):
#     """
#     Load historical weather data from CSV file
    
#     Args:
#         file_path (str): Path to the CSV file containing historical weather data
        
#     Returns:
#         pd.DataFrame: Processed historical weather data
#     """
#     # Load the data
#     df = pd.read_csv(file_path)
    
#     # Convert date column to datetime (assuming there's a date column)
#     if 'date' in df.columns:
#         df['date'] = pd.to_datetime(df['date'])
#     else:
#         # If no date column exists, try to find it or create one
#         date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
#         if date_columns:
#             df['date'] = pd.to_datetime(df[date_columns[0]])
#         else:
#             raise ValueError("No date column found in the CSV file")
    
#     # Extract month and day features for seasonality
#     df['month'] = df['date'].dt.month
#     df['day'] = df['date'].dt.day
#     df['day_of_year'] = df['date'].dt.dayofyear
    
#     return df

# # Function to fetch current weather data from WeatherAPI
# def fetch_current_weather(api_key, location):
#     """
#     Fetch current weather data from WeatherAPI
    
#     Args:
#         api_key (str): Your WeatherAPI API key
#         location (str): Location name (e.g., "Parang,Calapan City,Oriental Mindoro")
        
#     Returns:
#         dict: Current weather data
#     """
#     # First, get current weather data
#     current_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no"
#     current_response = requests.get(current_url)
    
#     # Then, get forecast for today to get min/max temps
#     forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=no"
#     forecast_response = requests.get(forecast_url)
    
#     if current_response.status_code == 200 and forecast_response.status_code == 200:
#         current_data = current_response.json()
#         forecast_data = forecast_response.json()
        
#         # Combine the data
#         combined_data = {
#             'current': current_data['current'],
#             'forecast': forecast_data['forecast']['forecastday'][0]
#         }
        
#         return combined_data
#     else:
#         raise Exception(f"Failed to fetch data. Current: {current_response.status_code}, Forecast: {forecast_response.status_code}")

# # Function to map WeatherAPI data to our desired format
# def map_weather_data(weather_data):
#     """
#     Map WeatherAPI data to our desired format
    
#     Args:
#         weather_data (dict): Weather data from WeatherAPI
        
#     Returns:
#         dict: Mapped weather data
#     """
#     mapped_data = {
#         'temperature_max': weather_data['forecast']['day']['maxtemp_c'],
#         'temperature_min': weather_data['forecast']['day']['mintemp_c'],
#         'rainfall': weather_data['forecast']['day']['totalprecip_mm'],
#         'precipitation_hours': weather_data['forecast']['day']['daily_will_it_rain'] * 24 / 100,  # Approximation based on chance of rain
#         'wind_speed': weather_data['current']['wind_kph'],
#         'cloud_cover': weather_data['current']['cloud'],
#         'humidity': weather_data['current']['humidity'],
#         'pressure': weather_data['current']['pressure_mb'],
#         'snowfall': 0  # Default to 0 since this data might not be available directly
#     }
#     return mapped_data

# # Function to get weather forecast features
# def prepare_forecast_features(historical_df, current_weather, days=30):
#     """
#     Prepare features for weather forecasting
    
#     Args:
#         historical_df (pd.DataFrame): Historical weather data
#         current_weather (dict): Current weather conditions
#         days (int): Number of days to forecast
        
#     Returns:
#         pd.DataFrame: Features for forecasting
#     """
#     # Get current date
#     current_date = datetime.now()
    
#     # Create dataframe for forecast dates
#     forecast_dates = [current_date + timedelta(days=i) for i in range(1, days+1)]
#     forecast_df = pd.DataFrame({'date': forecast_dates})
    
#     # Extract features
#     forecast_df['month'] = forecast_df['date'].dt.month
#     forecast_df['day'] = forecast_df['date'].dt.day
#     forecast_df['day_of_year'] = forecast_df['date'].dt.dayofyear
    
#     # Map current weather data to our format
#     mapped_weather = map_weather_data(current_weather)
    
#     # Add current weather as lagged features
#     for param in mapped_weather:
#         forecast_df[f'prev_{param}'] = mapped_weather[param]
    
#     return forecast_df

# # Function to train weather forecasting models
# def train_forecast_models(historical_df):
#     """
#     Train models for forecasting weather parameters
    
#     Args:
#         historical_df (pd.DataFrame): Historical weather data
        
#     Returns:
#         dict: Trained models for each weather parameter
#     """
#     # Target weather parameters
#     target_columns = [
#         'temperature_max', 'temperature_min', 'rainfall', 
#         'precipitation_hours', 'snowfall', 'wind_speed', 
#         'cloud_cover', 'humidity', 'pressure'
#     ]
    
#     # Create lagged features for previous day's weather
#     for col in target_columns:
#         if col in historical_df.columns:
#             historical_df[f'prev_{col}'] = historical_df[col].shift(1)
#         else:
#             print(f"Warning: Column '{col}' not found in historical data. Creating empty column.")
#             historical_df[col] = 0  # Create with default values
#             historical_df[f'prev_{col}'] = 0
    
#     # Drop rows with NaN values
#     historical_df = historical_df.dropna()
    
#     # Define features (seasonal + previous day's weather)
#     features = ['month', 'day', 'day_of_year']
#     for col in target_columns:
#         features.append(f'prev_{col}')
    
#     # Initialize models
#     models = {}
#     scalers = {}
    
#     # Train a model for each target variable
#     for target in target_columns:
#         # Check if target column exists
#         if target not in historical_df.columns:
#             print(f"Warning: Column '{target}' not found in historical data. Skipping model training.")
#             continue
            
#         # Split features and target
#         X = historical_df[features]
#         y = historical_df[target]
        
#         # Split data
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
#         # Scale features
#         scaler = StandardScaler()
#         X_train_scaled = scaler.fit_transform(X_train)
#         X_test_scaled = scaler.transform(X_test)
        
#         # Train model
#         model = RandomForestRegressor(n_estimators=100, random_state=42)
#         model.fit(X_train_scaled, y_train)
        
#         # Store model and scaler
#         models[target] = model
#         scalers[target] = scaler
        
#         # Evaluate model
#         train_score = model.score(X_train_scaled, y_train)
#         test_score = model.score(X_test_scaled, y_test)
#         print(f"Model for {target}: Train R² = {train_score:.4f}, Test R² = {test_score:.4f}")
    
#     return models, scalers, features

# # Function to make weather forecasts
# def forecast_weather(forecast_df, models, scalers, features):
#     """
#     Generate weather forecasts for the next 30 days
    
#     Args:
#         forecast_df (pd.DataFrame): Features for forecasting
#         models (dict): Trained models for each weather parameter
#         scalers (dict): Scalers for each model
#         features (list): Feature names
        
#     Returns:
#         pd.DataFrame: Weather forecasts
#     """
#     # Make a copy of the forecast dataframe
#     results_df = forecast_df.copy()
    
#     # Target weather parameters
#     target_columns = [
#         'temperature_max', 'temperature_min', 'rainfall', 
#         'precipitation_hours', 'snowfall', 'wind_speed', 
#         'cloud_cover', 'humidity', 'pressure'
#     ]
    
#     # Initialize missing target columns with zeros
#     for target in target_columns:
#         if target not in results_df.columns:
#             results_df[target] = 0
    
#     # Loop through each day and predict weather
#     for i in range(len(results_df)):
#         row = results_df.iloc[[i]]
        
#         # Make predictions for each target
#         for target in target_columns:
#             if target in models:
#                 # Ensure all features are present in the row
#                 feature_values = []
#                 for feat in features:
#                     if feat not in row.columns:
#                         row[feat] = 0
                
#                 X = row[features]
#                 X_scaled = scalers[target].transform(X)
#                 prediction = models[target].predict(X_scaled)[0]
                
#                 # Ensure predictions are reasonable
#                 if target == 'humidity' or target == 'cloud_cover':
#                     prediction = max(0, min(100, prediction))  # Clamp between 0-100%
#                 elif target == 'precipitation_hours':
#                     prediction = max(0, min(24, prediction))  # Clamp between 0-24 hours
#                 elif 'temperature' in target or target in ['rainfall', 'snowfall', 'wind_speed', 'pressure']:
#                     prediction = max(0, prediction)  # Ensure non-negative values
                
#                 # Store prediction
#                 results_df.loc[results_df.index[i], target] = prediction
        
#         # If not the last day, update lagged features for next day
#         if i < len(results_df) - 1:
#             for target in target_columns:
#                 if target in models:
#                     results_df.loc[results_df.index[i+1], f'prev_{target}'] = results_df.loc[results_df.index[i], target]
    
#     return results_df

# # Function to evaluate forecast accuracy (added missing function)
# def evaluate_forecast_accuracy(historical_df, models, scalers, features):
#     """
#     Evaluate the accuracy of forecasting models on historical data
    
#     Args:
#         historical_df (pd.DataFrame): Historical weather data
#         models (dict): Trained models for each weather parameter
#         scalers (dict): Scalers for each model
#         features (list): Feature names
        
#     Returns:
#         dict: Accuracy metrics for each target
#         pd.DataFrame: Comparison of actual vs. predicted values
#     """
#     # Target weather parameters
#     target_columns = [
#         'temperature_max', 'temperature_min', 'rainfall', 
#         'precipitation_hours', 'snowfall', 'wind_speed', 
#         'cloud_cover', 'humidity', 'pressure'
#     ]
    
#     # Initialize results
#     accuracy_metrics = {}
#     comparison_data = []
    
#     # Get the most recent 30 days of data for testing
#     test_df = historical_df.sort_values('date', ascending=False).head(30).sort_values('date')
    
#     # For each target, compare predicted vs actual
#     for target in target_columns:
#         if target not in models or target not in historical_df.columns:
#             continue
            
#         predictions = []
#         actuals = []
        
#         # Prepare data for forecasting
#         forecast_data = test_df.copy()
        
#         # Ensure all required features are present
#         for feat in features:
#             if feat not in forecast_data.columns:
#                 forecast_data[feat] = 0
        
#         # Make one-day-ahead predictions for each day in the test period
#         for i in range(len(forecast_data)):
#             # Get features for current day
#             X = forecast_data.iloc[[i]][features]
            
#             # Skip if any NaN values
#             if X.isna().any().any():
#                 continue
                
#             # Scale features
#             X_scaled = scalers[target].transform(X)
            
#             # Make prediction
#             prediction = models[target].predict(X_scaled)[0]
            
#             # Apply constraints
#             if target == 'humidity' or target == 'cloud_cover':
#                 prediction = max(0, min(100, prediction))
#             elif target == 'precipitation_hours':
#                 prediction = max(0, min(24, prediction))
#             elif 'temperature' in target or target in ['rainfall', 'snowfall', 'wind_speed', 'pressure']:
#                 prediction = max(0, prediction)
            
#             # Get actual value
#             actual = forecast_data.iloc[i][target]
            
#             # Skip if actual value is NaN
#             if pd.isna(actual):
#                 continue
                
#             # Store prediction and actual
#             predictions.append(prediction)
#             actuals.append(actual)
            
#             # Add to comparison data
#             comparison_data.append({
#                 'date': forecast_data.iloc[i]['date'],
#                 'target': target,
#                 'predicted': prediction,
#                 'actual': actual
#             })
            
#         # Skip if no valid predictions
#         if not predictions or not actuals:
#             continue
            
#         # Calculate metrics
#         mae = mean_absolute_error(actuals, predictions)
#         rmse = np.sqrt(mean_squared_error(actuals, predictions))
#         r2 = r2_score(actuals, predictions)
        
#         # Store metrics
#         accuracy_metrics[target] = {
#             'mae': mae,
#             'rmse': rmse,
#             'r2': r2
#         }
        
#     # Create comparison dataframe
#     comparison_df = pd.DataFrame(comparison_data)
    
#     return accuracy_metrics, comparison_df

# # Function to visualize forecasts
# def visualize_forecasts(forecast_results):
#     """
#     Create visualizations of weather forecasts
    
#     Args:
#         forecast_results (pd.DataFrame): Weather forecast results
#     """
#     plt.figure(figsize=(15, 30))
    
#     # Temperature max/min forecast
#     plt.subplot(9, 1, 1)
#     plt.plot(forecast_results['date'], forecast_results['temperature_max'], 'r-', label='Max')
#     plt.plot(forecast_results['date'], forecast_results['temperature_min'], 'b-', label='Min')
#     plt.title('Temperature Forecast (°C)')
#     plt.legend()
#     plt.grid(True)
    
#     # Rainfall forecast
#     plt.subplot(9, 1, 2)
#     plt.bar(forecast_results['date'], forecast_results['rainfall'], color='blue', alpha=0.7)
#     plt.title('Rainfall Forecast (mm)')
#     plt.grid(True)
    
#     # Precipitation hours forecast
#     plt.subplot(9, 1, 3)
#     plt.bar(forecast_results['date'], forecast_results['precipitation_hours'], color='cyan', alpha=0.7)
#     plt.title('Precipitation Hours Forecast')
#     plt.grid(True)
    
#     # Snowfall forecast
#     plt.subplot(9, 1, 4)
#     plt.bar(forecast_results['date'], forecast_results['snowfall'], color='lightblue', alpha=0.7)
#     plt.title('Snowfall Forecast (cm)')
#     plt.grid(True)
    
#     # Wind speed forecast
#     plt.subplot(9, 1, 5)
#     plt.plot(forecast_results['date'], forecast_results['wind_speed'], 'g-')
#     plt.title('Wind Speed Forecast (km/h)')
#     plt.grid(True)
    
#     # Cloud cover forecast
#     plt.subplot(9, 1, 6)
#     plt.plot(forecast_results['date'], forecast_results['cloud_cover'], 'grey')
#     plt.title('Cloud Cover Forecast (%)')
#     plt.grid(True)
    
#     # Humidity forecast
#     plt.subplot(9, 1, 7)
#     plt.plot(forecast_results['date'], forecast_results['humidity'], 'purple')
#     plt.title('Humidity Forecast (%)')
#     plt.grid(True)
    
#     # Pressure forecast
#     plt.subplot(9, 1, 8)
#     plt.plot(forecast_results['date'], forecast_results['pressure'], 'y-')
#     plt.title('Pressure Forecast (mb)')
#     plt.grid(True)
    
#     plt.tight_layout()
#     plt.savefig('weather_forecast.png')
#     plt.show()

# # Main function to run the weather forecasting
# def main():
#     load_dotenv()
#     # Configuration
#     api_key = os.getenv("WEATHER_API_KEY")  # Replace with your actual API key
#     location = "Parang,Calapan City,Oriental Mindoro"
#     historical_data_path = "dataset.csv"  # Replace with your actual file path
    
#     # Load historical data
#     print("Loading historical weather data...")
#     historical_df = load_historical_data(historical_data_path)
    
#     # Fetch current weather data
#     print("Fetching current weather data...")
#     try:
#         current_weather = fetch_current_weather(api_key, location)
#         mapped_data = map_weather_data(current_weather)
#         print(f"Current data: Max Temp: {mapped_data['temperature_max']}°C, Min Temp: {mapped_data['temperature_min']}°C")
#     except Exception as e:
#         print(f"Error fetching current weather: {e}")
#         return
    
#     # Train forecasting models
#     print("Training forecasting models...")
#     models, scalers, features = train_forecast_models(historical_df)
    
#     # Prepare features for forecasting
#     print("Preparing forecast features...")
#     forecast_df = prepare_forecast_features(historical_df, current_weather)
    
#     # Generate forecasts
#     print("Generating 30-day weather forecast...")
#     forecast_results = forecast_weather(forecast_df, models, scalers, features)
    
#     # Evaluate forecast accuracy
#     print("Evaluating forecast accuracy...")
#     try:
#         accuracy_metrics, comparison_df = evaluate_forecast_accuracy(historical_df, models, scalers, features)
#         print("\nForecast Accuracy Metrics:")
#         for target, metrics in accuracy_metrics.items():
#             print(f"{target}: MAE = {metrics['mae']:.2f}, RMSE = {metrics['rmse']:.2f}, R² = {metrics['r2']:.2f}")
#     except Exception as e:
#         print(f"Warning: Could not evaluate forecast accuracy: {e}")
#         accuracy_metrics = {}
#         comparison_df = pd.DataFrame()
    
#     # Save forecast results to CSV
#     forecast_results.to_csv('weather_forecast_results.csv', index=False)
#     print("Forecast results saved to 'weather_forecast_results.csv'")
    
#     # Visualize forecasts
#     print("Creating forecast visualizations...")
#     visualize_forecasts(forecast_results)
    
#     # Print forecast summary
#     print("\nWeather Forecast Summary for Next Week:")
#     for i in range(7):
#         date = forecast_results['date'].iloc[i].strftime('%Y-%m-%d')
#         temp_max = forecast_results['temperature_max'].iloc[i]
#         temp_min = forecast_results['temperature_min'].iloc[i]
#         rainfall = forecast_results['rainfall'].iloc[i]
#         precip_hours = forecast_results['precipitation_hours'].iloc[i]
        
#         print(f"{date}: {temp_min:.1f}°C to {temp_max:.1f}°C, {rainfall:.1f}mm rainfall over {precip_hours:.1f} hours")

# if __name__ == "__main__":
#     main()

#=====================================================#




# import os
# import requests
# import pandas as pd
# import numpy as np
# import datetime
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import mean_absolute_error
# from sklearn.linear_model import LinearRegression
# import joblib

# # Step 1: Load the model and scaler
# model = joblib.load("weather_model.pkl")  # Replace with your model file
# scaler = joblib.load("scaler.pkl")  # Replace with your scaler file

# # Step 2: Define the function to fetch the current weather data from WeatherAPI
# def fetch_current_weather():
#     api_key = os.getenv("WEATHER_API_KEY")  # Replace with your WeatherAPI key
#     location = 'Parang, Calapan City, Oriental Mindoro'
#     url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"

#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()

#         current_weather = {
#             "temperature_max": data["current"]["temp_c"],  # Max temperature in Celsius
#             "temperature_min": data["current"]["temp_c"],  # Min temperature in Celsius
#             "rainfall": data["current"]["precip_mm"],  # Precipitation in mm
#             "precipitation_hours": data["current"]["precip_mm"],  # Precipitation hours
#             "snowfall": data["current"].get("snow_mm", 0),  # Snowfall in mm (Weather API returns 0 if no snow)
#             "wind_speed": data["current"]["wind_kph"],  # Wind speed in km/h
#             "cloud_cover": data["current"]["cloud"],  # Cloud cover percentage
#             "humidity": data["current"]["humidity"],  # Humidity in percentage
#             "pressure": data["current"]["pressure_mb"]  # Pressure in mb
#         }
#         return current_weather
#     else:
#         print(f"Error fetching current weather: {response.status_code}")
#         return None

# # Step 3: Fetch the current weather data
# current_weather = fetch_current_weather()

# if current_weather:
#     # Step 4: Convert the current weather data to a DataFrame
#     current_weather_df = pd.DataFrame([current_weather])

#     # Step 5: Add the missing features (day_of_year, month, weekday) to match training features
#     current_weather_df['day_of_year'] = datetime.datetime.now().timetuple().tm_yday
#     current_weather_df['month'] = datetime.datetime.now().month
#     current_weather_df['weekday'] = datetime.datetime.now().weekday()

#     # Step 6: Scale the current weather data (with the added features)
#     current_weather_scaled = scaler.transform(current_weather_df)

#     # Step 7: Prepare the data for prediction (use last 30 days data to predict the next 30 days)
#     last_30_days = np.array([current_weather_scaled])

#     # Step 8: Predict the next 30 days using the model
#     forecast = model.predict(last_30_days)

#     # Step 9: Initialize list to store the forecast for the next 30 days
#     forecast_list = []

#     # Step 10: Forecasting for the next 30 days
#     for i in range(30):
#         forecast_reshaped = np.reshape(forecast, (1, -1))  # Reshape to (1, 9) as the model predicts multiple features
#         forecast_rescaled = scaler.inverse_transform(forecast_reshaped)

#         # Append the forecasted data for each day
#         forecast_list.append(forecast_rescaled[0])

#     # Step 11: Convert forecast data to a DataFrame
#     forecast_df = pd.DataFrame(forecast_list, columns=current_weather_df.columns)

#     # Step 12: Save forecast to a CSV file
#     forecast_df.to_csv('forecasted_weather_30_days.csv', index=False)

#     # Step 13: Print the current weather data
#     print(f"Current weather data: {current_weather}")

#     # Step 14: Print the forecast for the next 30 days
#     print(f"Forecast for the next 30 days:\n{forecast_df}")

#     # Optional: Calculate and print Mean Absolute Error (MAE) if you have actual weather data for comparison
#     actual_data = pd.read_csv('actual_weather_data.csv')  # Replace with your actual weather data file
#     y_true = actual_data.iloc[:30]  # Actual weather data for the first 30 days
#     y_pred = forecast_df  # Predicted weather data for the first 30 days

#     mae = mean_absolute_error(y_true, y_pred)
#     print(f"Mean Absolute Error: {mae}")

# else:
#     print("Unable to fetch current weather data.")
