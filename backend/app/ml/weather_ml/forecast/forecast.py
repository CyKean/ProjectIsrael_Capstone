
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
#     plt.close()

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






import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import os
from dotenv import load_dotenv
from joblib import dump, load
import warnings
warnings.filterwarnings('ignore')


def load_historical_data(file_path):
    """Load and preprocess historical weather data."""
    df = pd.read_csv(file_path)
    
    # Find date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    else:
        date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_columns:
            df['date'] = pd.to_datetime(df[date_columns[0]])
        else:
            raise ValueError("No date column found in the CSV file")
    
    # Sort by date to ensure time-based operations work correctly
    df = df.sort_values('date')
    
    # Extract time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_year'] = df['date'].dt.dayofyear
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Create cyclical features for seasonal patterns
    df['month_sin'] = np.sin(2 * np.pi * df['month']/12)
    df['month_cos'] = np.cos(2 * np.pi * df['month']/12)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_year']/365)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_year']/365)
    
    # Handle missing values
    for col in df.columns:
        if df[col].dtype in [np.float64, np.int64] and col != 'date':
            df[col] = df[col].fillna(df[col].median())
    
    # Create lagged features for all target columns
    target_columns = ['temperature_max', 'temperature_min', 'rainfall', 'precipitation_hours', 
                      'snowfall', 'wind_speed', 'cloud_cover', 'humidity', 'pressure']
    
    # Create 1, 2, 3, 7 and 365 day lags (previous day, 2 days ago, week ago, year ago)
    for col in target_columns:
        if col in df.columns:
            df[f'{col}_lag1'] = df[col].shift(1)
            df[f'{col}_lag2'] = df[col].shift(2)
            df[f'{col}_lag3'] = df[col].shift(3)
            df[f'{col}_lag7'] = df[col].shift(7)
            
            # Add a year ago if we have enough data
            if len(df) > 365:
                df[f'{col}_lag365'] = df[col].shift(365)
            
            # Add rolling means for different windows
            df[f'{col}_rolling3'] = df[col].rolling(window=3).mean().shift(1)
            df[f'{col}_rolling7'] = df[col].rolling(window=7).mean().shift(1)
            df[f'{col}_rolling14'] = df[col].rolling(window=14).mean().shift(1)
            df[f'{col}_rolling30'] = df[col].rolling(window=30).mean().shift(1)
    
    # Drop rows with NaN values created by the lag operations
    df = df.dropna()
    
    return df


def fetch_current_weather(api_key, location):
    """Fetch current weather data from the API."""
    current_url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no"
    forecast_url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=no"
    
    try:
        current_response = requests.get(current_url, timeout=10)
        forecast_response = requests.get(forecast_url, timeout=10)
        
        if current_response.status_code == 200 and forecast_response.status_code == 200:
            return {
                'current': current_response.json()['current'],
                'forecast': forecast_response.json()['forecast']['forecastday'][0]
            }
        else:
            raise Exception(f"Failed to fetch data from WeatherAPI. Status codes: {current_response.status_code}, {forecast_response.status_code}")
    except Exception as e:
        raise Exception(f"Network error while fetching weather data: {e}")


def map_weather_data(weather_data):
    """Map API weather data to our model features."""
    return {
        'temperature_max': weather_data['forecast']['day']['maxtemp_c'],
        'temperature_min': weather_data['forecast']['day']['mintemp_c'],
        'rainfall': weather_data['forecast']['day']['totalprecip_mm'],
        'precipitation_hours': weather_data['forecast']['day']['daily_will_it_rain'] * 24 / 100,
        'wind_speed': weather_data['current']['wind_kph'],
        'cloud_cover': weather_data['current']['cloud'],
        'humidity': weather_data['current']['humidity'],
        'pressure': weather_data['current']['pressure_mb'],
        'snowfall': 0
    }


def select_best_model_for_target(X_train, X_test, y_train, y_test, target_name):
    """Select the best model for a given target variable."""
    # Define different model candidates
    models = {
        'RandomForest': RandomForestRegressor(random_state=42),
        'GradientBoosting': GradientBoostingRegressor(random_state=42),
        'ElasticNet': ElasticNet(random_state=42)
    }
    
    best_score = -float('inf')
    best_model = None
    best_model_name = None
    model_results = {}
    
    for name, model in models.items():
        # If we have a small dataset or simple targets, go with simpler models
        if len(X_train) < 500 and name == 'RandomForest':
            model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
        
        # Fit the model
        model.fit(X_train, y_train)
        
        # Evaluate
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        
        model_results[name] = {
            'train_r2': train_score,
            'test_r2': test_score,
            'rmse': rmse,
            'mae': mae
        }
        
        if test_score > best_score:
            best_score = test_score
            best_model = model
            best_model_name = name
    
    print(f"\nModel selection for {target_name}:")
    for name, metrics in model_results.items():
        print(f"  {name}: Train R² = {metrics['train_r2']:.4f}, Test R² = {metrics['test_r2']:.4f}, RMSE = {metrics['rmse']:.4f}")
    print(f"  Selected model: {best_model_name} (Test R² = {best_score:.4f})")
    
    # If all models perform poorly, fall back to a simpler model
    if best_score < 0.3 and target_name in ['rainfall', 'precipitation_hours', 'snowfall']:
        print(f"  Low performance for {target_name}. Using seasonal baseline model.")
        # For rainfall-related features, we'll use a monthly average-based model
        best_model = SeasonalFallbackModel()
        best_model.fit(X_train, y_train)
    
    return best_model


class SeasonalFallbackModel:
    """Fallback model for seasonal data when ML models fail."""
    
    def __init__(self):
        self.monthly_averages = {}
        self.overall_average = 0
    
    def fit(self, X, y):
        """Compute monthly averages of the target variable."""
        # Extract month column
        month_col = None
        for col in X.columns:
            if col == 'month':
                month_col = col
                break
        
        if month_col is None:
            self.overall_average = np.mean(y)
            return self
        
        # Compute monthly averages
        combined = pd.DataFrame({'month': X[month_col], 'target': y})
        self.monthly_averages = combined.groupby('month')['target'].mean().to_dict()
        self.overall_average = np.mean(y)
        return self
    
    def predict(self, X):
        """Predict using monthly averages."""
        predictions = []
        
        month_col = None
        for col in X.columns:
            if col == 'month':
                month_col = col
                break
        
        if month_col is None:
            return np.full(len(X), self.overall_average)
        
        for idx, row in X.iterrows():
            month = row[month_col]
            if month in self.monthly_averages:
                predictions.append(self.monthly_averages[month])
            else:
                predictions.append(self.overall_average)
        
        return np.array(predictions)
    
    def score(self, X, y):
        """Calculate R2 score."""
        y_pred = self.predict(X)
        return r2_score(y, y_pred)


def prepare_base_features(df, current_date):
    """Prepare base time features for forecast dates."""
    # Create time features for forecast date
    result = {}
    result['year'] = current_date.year
    result['month'] = current_date.month
    result['day'] = current_date.day
    result['day_of_year'] = current_date.timetuple().tm_yday
    result['day_of_week'] = current_date.weekday()
    result['is_weekend'] = 1 if current_date.weekday() >= 5 else 0
    
    # Create cyclical features
    result['month_sin'] = np.sin(2 * np.pi * current_date.month/12)
    result['month_cos'] = np.cos(2 * np.pi * current_date.month/12)
    result['day_sin'] = np.sin(2 * np.pi * result['day_of_year']/365)
    result['day_cos'] = np.cos(2 * np.pi * result['day_of_year']/365)
    
    return result


def prepare_forecast_features(historical_df, current_weather, days=30):
    """Prepare features for the forecast period."""
    current_date = datetime.now()
    forecast_dates = [current_date + timedelta(days=i) for i in range(1, days+1)]
    forecast_df = pd.DataFrame({'date': forecast_dates})
    
    # Add base time features for each date
    base_features = []
    for date in forecast_dates:
        base_features.append(prepare_base_features(historical_df, date))
    
    base_df = pd.DataFrame(base_features)
    forecast_df = pd.concat([forecast_df, base_df], axis=1)
    
    # Map the current weather data to use as initial lag values
    mapped_weather = map_weather_data(current_weather)
    target_columns = ['temperature_max', 'temperature_min', 'rainfall', 'precipitation_hours', 
                      'snowfall', 'wind_speed', 'cloud_cover', 'humidity', 'pressure']
    
    # Add lag features starting with current data
    for target in target_columns:
        forecast_df[f'{target}_lag1'] = np.nan  # Will be populated during forecasting
        forecast_df[f'{target}_lag2'] = np.nan
        forecast_df[f'{target}_lag3'] = np.nan
        forecast_df[f'{target}_lag7'] = np.nan
        forecast_df[f'{target}_rolling3'] = np.nan
        forecast_df[f'{target}_rolling7'] = np.nan
        forecast_df[f'{target}_rolling14'] = np.nan
        forecast_df[f'{target}_rolling30'] = np.nan
    
    return forecast_df


def train_forecast_models(historical_df):
    """Train models for each target variable with feature importance analysis."""
    target_columns = ['temperature_max', 'temperature_min', 'rainfall', 'precipitation_hours', 
                     'snowfall', 'wind_speed', 'cloud_cover', 'humidity', 'pressure']
    
    # Identify all available features (excluding target variables and date)
    all_features = [col for col in historical_df.columns 
                   if col not in target_columns and col != 'date']
    
    models = {}
    scalers = {}
    feature_importances = {}
    feature_sets = {}
    
    # Split the data chronologically - important for time series
    train_size = int(len(historical_df) * 0.8)
    historical_df_train = historical_df.iloc[:train_size]
    historical_df_test = historical_df.iloc[train_size:]
    
    for target in target_columns:
        if target not in historical_df.columns:
            print(f"Target column '{target}' not found in historical data, skipping.")
            continue
        
        print(f"\nTraining model for {target}...")
        
        # Get all features except the current target and other targets
        features = [col for col in all_features if col != target]
        
        X_train = historical_df_train[features]
        y_train = historical_df_train[target]
        X_test = historical_df_test[features]
        y_test = historical_df_test[target]
        
        # Create a scaler for this target
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Convert back to DataFrame to keep column names
        X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X_train.columns)
        X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X_test.columns)
        
        # Select best model for this target
        model = select_best_model_for_target(X_train_scaled_df, X_test_scaled_df, y_train, y_test, target)
        
        # Save for later use
        models[target] = model
        scalers[target] = scaler
        feature_sets[target] = features
        
        # If it's a tree-based model, get feature importances
        if hasattr(model, 'feature_importances_'):
            # Get feature importances
            importances = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature': features,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            # Save top 10 feature importances for visualization
            feature_importances[target] = feature_importance_df.head(10)
            
            print("Top 5 important features:")
            for idx, row in feature_importance_df.head(5).iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
    
    return models, scalers, feature_sets, feature_importances


def forecast_weather(forecast_df, models, scalers, feature_sets, historical_df):
    """Generate weather forecasts using the trained models."""
    results_df = forecast_df.copy()
    target_columns = ['temperature_max', 'temperature_min', 'rainfall', 'precipitation_hours', 
                     'snowfall', 'wind_speed', 'cloud_cover', 'humidity', 'pressure']
    
    # Initialize target columns in results
    for target in target_columns:
        results_df[target] = 0.0
    
    # Get the last 30 days of historical data for rolling calculations
    last_30_days = historical_df.tail(30).copy()
    
    # Initialize lag features with historical data
    for target in target_columns:
        if f'{target}_lag1' in results_df.columns:
            results_df.loc[0, f'{target}_lag1'] = last_30_days[target].iloc[-1]
        if f'{target}_lag2' in results_df.columns:
            results_df.loc[0, f'{target}_lag2'] = last_30_days[target].iloc[-2]
        if f'{target}_lag3' in results_df.columns:
            results_df.loc[0, f'{target}_lag3'] = last_30_days[target].iloc[-3]
        if f'{target}_lag7' in results_df.columns:
            results_df.loc[0, f'{target}_lag7'] = last_30_days[target].iloc[-7]
        
        # Initialize rolling averages
        if f'{target}_rolling3' in results_df.columns:
            results_df.loc[0, f'{target}_rolling3'] = last_30_days[target].tail(3).mean()
        if f'{target}_rolling7' in results_df.columns:
            results_df.loc[0, f'{target}_rolling7'] = last_30_days[target].tail(7).mean()
        if f'{target}_rolling14' in results_df.columns:
            results_df.loc[0, f'{target}_rolling14'] = last_30_days[target].tail(14).mean()
        if f'{target}_rolling30' in results_df.columns:
            results_df.loc[0, f'{target}_rolling30'] = last_30_days[target].tail(30).mean()
    
    # Fill remaining NaNs with 0
    results_df = results_df.fillna(0)
    
    # Iterate through days to forecast
    for i in range(len(results_df)):
        current_row = results_df.iloc[[i]]
        
        for target in target_columns:
            if target in models:
                features = feature_sets[target]
                pred_row = pd.DataFrame(index=[0])
                
                # Build feature row with proper column order
                for feat in features:
                    if feat in current_row.columns:
                        value = current_row[feat].values[0]
                        pred_row[feat] = value if not np.isnan(value) else 0
                    else:
                        pred_row[feat] = 0
                
                # Ensure column order matches training data
                pred_row = pred_row[features].fillna(0)
                
                # Scale features and maintain DataFrame structure
                try:
                    pred_row_scaled = scalers[target].transform(pred_row)
                except ValueError:
                    pred_row_scaled = pred_row.values  # Fallback for non-scaled models
                
                # Convert back to DataFrame with proper columns
                pred_row_scaled_df = pd.DataFrame(pred_row_scaled, columns=features)
                
                # Make prediction
                try:
                    prediction = models[target].predict(pred_row_scaled_df)[0]
                except AttributeError:
                    # Handle models that expect numpy arrays directly
                    prediction = models[target].predict(pred_row_scaled_df.values)[0]
                
                # Apply constraints
                if target in ['humidity', 'cloud_cover']:
                    prediction = max(0, min(100, prediction))
                elif target == 'precipitation_hours':
                    prediction = max(0, min(24, prediction))
                elif target in ['rainfall', 'snowfall']:
                    prediction = max(0, prediction)
                
                results_df.at[results_df.index[i], target] = float(prediction)
        
        # Update lag features for next day
        if i < len(results_df) - 1:
            current_values = {target: results_df.at[results_df.index[i], target] 
                             for target in target_columns}
            
            # Update lag features
            for target in target_columns:
                # Shift existing lag values
                if f'{target}_lag1' in results_df.columns:
                    results_df.at[results_df.index[i+1], f'{target}_lag1'] = current_values[target]
                if f'{target}_lag2' in results_df.columns and i >= 0:
                    results_df.at[results_df.index[i+1], f'{target}_lag2'] = results_df.at[results_df.index[i], f'{target}_lag1']
                if f'{target}_lag3' in results_df.columns and i >= 1:
                    results_df.at[results_df.index[i+1], f'{target}_lag3'] = results_df.at[results_df.index[i], f'{target}_lag2']
                if f'{target}_lag7' in results_df.columns and i >= 6:
                    results_df.at[results_df.index[i+1], f'{target}_lag7'] = results_df.at[results_df.index[i-6], target]
                
                # Update rolling averages (FIXED HERE)
                window_data = pd.concat([
                    last_30_days[target].tail(29),
                    pd.Series([current_values[target]])])
                if f'{target}_rolling3' in results_df.columns:
                    results_df.at[results_df.index[i+1], f'{target}_rolling3'] = window_data.tail(3).mean()
                if f'{target}_rolling7' in results_df.columns:
                    results_df.at[results_df.index[i+1], f'{target}_rolling7'] = window_data.tail(7).mean()
                if f'{target}_rolling14' in results_df.columns:
                    results_df.at[results_df.index[i+1], f'{target}_rolling14'] = window_data.tail(14).mean()
                if f'{target}_rolling30' in results_df.columns:
                    results_df.at[results_df.index[i+1], f'{target}_rolling30'] = window_data.tail(30).mean()
            
            # Update historical data for next iteration
            new_row = last_30_days.iloc[-1:].copy()
            for target in target_columns:
                new_row[target] = current_values[target]
            new_row['date'] = results_df.at[results_df.index[i], 'date']
            last_30_days = pd.concat([last_30_days, new_row]).iloc[1:]  # Maintain 30-day window
    
    return results_df


def visualize_forecasts(forecast_results, models, feature_sets, historical_df=None, n_past_days=30):
    """Create visualizations of the forecasted weather data with improved plots."""
    # Set style for better looking plots
    sns.set(style="whitegrid")
    plt.rcParams.update({'font.size': 12})
    
    # Create a figure with subplots
    fig = plt.figure(figsize=(15, 25))
    
    # If historical data is provided, include it in the plots
    if historical_df is not None and len(historical_df) > 0:
        # Get the last n_past_days of historical data
        past_df = historical_df.sort_values('date').tail(n_past_days)
        has_historical = True
    else:
        has_historical = False
    
    # Convert dates for better x-axis labeling
    forecast_results['date_str'] = forecast_results['date'].dt.strftime('%m-%d')
    if has_historical:
        past_df['date_str'] = past_df['date'].dt.strftime('%m-%d')
    
    # Plot 1: Temperature
    ax1 = plt.subplot(5, 1, 1)
    plt.plot(forecast_results['date_str'], forecast_results['temperature_max'], 'r-', marker='o', markersize=5, label='Max Forecast')
    plt.plot(forecast_results['date_str'], forecast_results['temperature_min'], 'b-', marker='o', markersize=5, label='Min Forecast')
    
    if has_historical:
        plt.plot(past_df['date_str'], past_df['temperature_max'], 'r--', alpha=0.6, label='Max Historical')
        plt.plot(past_df['date_str'], past_df['temperature_min'], 'b--', alpha=0.6, label='Min Historical')
        plt.axvline(x=past_df['date_str'].iloc[-1], color='black', linestyle='--', alpha=0.5, label='Forecast Start')
    
    plt.title('Temperature Forecast (°C)', fontsize=16, fontweight='bold')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    
    # Plot 2: Rainfall and Precipitation Hours
    ax2 = plt.subplot(5, 1, 2)
    width = 0.35
    
    # Rainfall bars
    rain_bars = plt.bar(forecast_results['date_str'], forecast_results['rainfall'], width, color='blue', alpha=0.7, label='Rainfall (mm)')
    
    # Add text annotations for significant rainfall
    for i, v in enumerate(forecast_results['rainfall']):
        if v > 5:  # Only annotate significant rainfall
            plt.text(i, v + 0.5, f"{v:.1f}", ha='center', va='bottom', fontsize=10)
    
    # Set up secondary y-axis for precipitation hours
    ax2_twin = ax2.twinx()
    precip_line = ax2_twin.plot(forecast_results['date_str'], forecast_results['precipitation_hours'], 'c-', marker='s', markersize=5, label='Precipitation Hours')
    
    if has_historical:
        hist_rain = plt.bar([i - width/2 for i in range(len(past_df))], past_df['rainfall'], width, color='blue', alpha=0.3, label='Historical Rainfall')
        hist_precip = ax2_twin.plot(past_df['date_str'], past_df['precipitation_hours'], 'c--', alpha=0.6, label='Historical Precip Hours')
        plt.axvline(x=past_df['date_str'].iloc[-1], color='black', linestyle='--', alpha=0.5)
    
    # Combine legends from both y-axes
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.title('Rainfall and Precipitation', fontsize=16, fontweight='bold')
    ax2.set_ylabel('Rainfall (mm)')
    ax2_twin.set_ylabel('Precipitation Hours')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Plot 3: Wind Speed
    ax3 = plt.subplot(5, 1, 3)
    plt.plot(forecast_results['date_str'], forecast_results['wind_speed'], 'g-', marker='d', markersize=5, label='Forecast')
    
    if has_historical:
        plt.plot(past_df['date_str'], past_df['wind_speed'], 'g--', alpha=0.6, label='Historical')
        plt.axvline(x=past_df['date_str'].iloc[-1], color='black', linestyle='--', alpha=0.5, label='Forecast Start')
    
    plt.title('Wind Speed Forecast (km/h)', fontsize=16, fontweight='bold')
    plt.ylabel('Wind Speed (km/h)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    
    # Plot 4: Cloud Cover and Humidity
    ax4 = plt.subplot(5, 1, 4)
    plt.plot(forecast_results['date_str'], forecast_results['cloud_cover'], color='gray', marker='o', markersize=5, label='Cloud Cover')
    plt.plot(forecast_results['date_str'], forecast_results['humidity'], color='purple', marker='s', markersize=5, label='Humidity')
    
    if has_historical:
        plt.plot(past_df['date_str'], past_df['cloud_cover'], color='gray', linestyle='--', alpha=0.6, label='Historical Cloud')
        plt.plot(past_df['date_str'], past_df['humidity'], color='purple', linestyle='--', alpha=0.6, label='Historical Humidity')
        plt.axvline(x=past_df['date_str'].iloc[-1], color='black', linestyle='--', alpha=0.5, label='Forecast Start')
    
    plt.title('Cloud Cover and Humidity (%)', fontsize=16, fontweight='bold')
    plt.ylabel('Percentage (%)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    
    # Plot 5: Pressure
    ax5 = plt.subplot(5, 1, 5)
    plt.plot(forecast_results['date_str'], forecast_results['pressure'], 'orange', marker='o', markersize=5, label='Forecast')
    
    if has_historical:
        plt.plot(past_df['date_str'], past_df['pressure'], 'orange', linestyle='--', alpha=0.6, label='Historical')
        plt.axvline(x=past_df['date_str'].iloc[-1], color='black', linestyle='--', alpha=0.5, label='Forecast Start')
    
    plt.title('Barometric Pressure Forecast (mb)', fontsize=16, fontweight='bold')
    plt.ylabel('Pressure (mb)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig('weather_forecast.png', dpi=300, bbox_inches='tight')
    
    # Create feature importance plots if available
    if models and feature_sets:
        plt.figure(figsize=(15, 12))
        for i, target in enumerate(['temperature_max', 'rainfall', 'wind_speed', 'humidity']):
            if target in models and hasattr(models[target], 'feature_importances_'):
                importances = pd.DataFrame({
                    'feature': feature_sets[target],
                    'importance': models[target].feature_importances_
                }).sort_values('importance', ascending=False).head(10)
                
                plt.subplot(2, 2, i+1)
                sns.barplot(x='importance', y='feature', data=importances)
                plt.title(f'Top Features for {target}')
        
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    
    plt.close('all')



def evaluate_models(historical_df, models, scalers, feature_sets):
    """Evaluate model performance on the test set."""
    # Use last 20% of data as test set
    test_size = int(len(historical_df) * 0.2)
    test_df = historical_df.tail(test_size).copy()
    
    results = {}
    target_columns = ['temperature_max', 'temperature_min', 'rainfall', 'precipitation_hours', 
                     'snowfall', 'wind_speed', 'cloud_cover', 'humidity', 'pressure']
    
    for target in target_columns:
        if target not in models:
            continue
            
        features = feature_sets[target]
        X_test = test_df[features]
        y_test = test_df[target]
        
        # Scale features
        X_test_scaled = scalers[target].transform(X_test)
        
        # Make predictions
        y_pred = models[target].predict(X_test_scaled)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results[target] = {
            'MAE': mae,
            'RMSE': rmse,
            'R²': r2
        }
    
    # Print evaluation results
    print("\nModel Evaluation Metrics on Test Set:")
    for target, metrics in results.items():
        print(f"  {target}:")
        for name, value in metrics.items():
            print(f"    {name}: {value:.4f}")
    
    return results

def main():
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")

    # ✅ Use coordinates instead of location name
    latitude = 13.401977220608616
    longitude = 121.22464223345575
    coordinates = f"{latitude},{longitude}"

    historical_data_path = "dataset.csv"

    print("Loading historical weather data...")
    historical_df = load_historical_data(historical_data_path)

    print("Fetching current weather data...")
    try:
        # ✅ Pass coordinates here
        current_weather = fetch_current_weather(api_key, coordinates)
        mapped_data = map_weather_data(current_weather)
        print(f"Current data: Max Temp: {mapped_data['temperature_max']}°C, Min Temp: {mapped_data['temperature_min']}°C")
    except Exception as e:
        print(f"Error fetching current weather: {e}")
        return

    print("Training forecasting models...")
    models, scalers, feature_sets, _ = train_forecast_models(historical_df)

    print("Preparing forecast features...")
    forecast_df = prepare_forecast_features(historical_df, current_weather)

    print("Generating 30-day weather forecast...")
    forecast_results = forecast_weather(forecast_df, models, scalers, feature_sets, historical_df)

    print("Creating forecast visualizations...")
    visualize_forecasts(forecast_results, models, feature_sets, historical_df)

    output_csv_path = os.path.join(os.getcwd(), "weather_forecast_results.csv")
    try:
        forecast_results.to_csv(output_csv_path, index=False)
        print(f"Forecast results saved to '{output_csv_path}'")
    except PermissionError:
        print(f"Permission denied: Cannot save file to '{output_csv_path}'. Please close the file if it's open and try again.")


if __name__ == "__main__":
    main()