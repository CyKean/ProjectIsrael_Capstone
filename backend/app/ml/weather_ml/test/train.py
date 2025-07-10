import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import (mean_squared_error, mean_absolute_error, 
                             r2_score, f1_score, precision_score, recall_score)
from tensorflow import keras
from tensorflow.keras import layers, Model, losses, metrics
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import Sequence
import joblib
import matplotlib.pyplot as plt

# Configuration
TARGET_COLS = ['temperature_max', 'rainfall', 'precipitation_hours',
               'snowfall', 'wind_speed', 'cloud_cover', 'humidity', 'pressure']
MODEL_SAVE_PATH = 'improved_weather_forecaster.keras'
SCALER_SAVE_PATH = 'improved_scalers.pkl'

# Custom preprocessing class
class WeatherPreprocessor:
    def __init__(self, target_cols, n_lags=3):
        self.target_cols = target_cols
        self.n_lags = n_lags
        self.feature_scalers = {}
        self.target_scalers = {}
        
    def create_features(self, df):
        # Time features
        df['day_of_year'] = df['date'].dt.dayofyear
        df['month'] = df['date'].dt.month
        
        # Cyclical features
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_year']/365)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_year']/365)
        df['month_sin'] = np.sin(2 * np.pi * (df['month']-1)/12)
        df['month_cos'] = np.cos(2 * np.pi * (df['month']-1)/12)
        
        # Meteorological features
        df['dew_point'] = df['temperature_max'] - ((100 - df['humidity'])/5)
        df['temp_pressure_ratio'] = df['temperature_max'] / df['pressure']
        
        # Lag features with rolling stats
        for col in self.target_cols:
            for lag in range(1, self.n_lags+1):
                df[f'{col}_lag_{lag}'] = df[col].shift(lag)
            df[f'{col}_rolling_mean_3'] = df[col].rolling(3).mean()
            df[f'{col}_rolling_std_3'] = df[col].rolling(3).std()
        
        df.dropna(inplace=True)
        return df

    def fit_transform(self, X, y):
        # Fit and transform features
        self.feature_scalers = {
            'minmax': MinMaxScaler().fit(X[['temperature_max', 'pressure', 'dew_point']]),
            'standard': StandardScaler().fit(X[['wind_speed', 'cloud_cover', 'temp_pressure_ratio']])
        }
        
        # Transform targets with individual scalers
        self.target_scalers = {
            col: MinMaxScaler() if col in ['temperature_max', 'pressure'] 
            else StandardScaler() for col in self.target_cols
        }
        
        # Apply transformations
        X_scaled = np.hstack([
            self.feature_scalers['minmax'].transform(X[['temperature_max', 'pressure', 'dew_point']]),
            self.feature_scalers['standard'].transform(X[['wind_speed', 'cloud_cover', 'temp_pressure_ratio']]),
            X[['day_sin', 'day_cos', 'month_sin', 'month_cos']].values
        ])
        
        y_scaled = np.hstack([
            scaler.transform(y[[col]].values) 
            for col, scaler in self.target_scalers.items()
        ])
        
        return X_scaled, y_scaled

# Custom model architecture
def build_multi_target_model(input_shape, n_targets):
    inputs = layers.Input(shape=input_shape)
    
    # Shared base network
    x = layers.Dense(256, activation='swish')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(128, activation='swish')(x)
    x = layers.Dropout(0.3)(x)
    
    # Variable-specific heads
    outputs = []
    for _ in range(n_targets):
        head = layers.Dense(64, activation='swish')(x)
        head = layers.Dense(32, activation='swish')(head)
        outputs.append(layers.Dense(1)(head))
        
    model = Model(inputs=inputs, outputs=outputs)
    
    # Custom loss weights (adjust based on priority)
    loss_weights = {
        'temperature_max': 1.5,  # Highest priority - key forecast element
        'rainfall': 1.2,         # Important for flood/agriculture warnings
        'precipitation_hours': 1.0,  # Moderate priority - related to rainfall
        'snowfall': 0.8,         # Lower priority - rare events/sparse data
        'wind_speed': 1.1,       # High priority for safety alerts
        'cloud_cover': 0.9,      # Moderate impact on solar/temperature
        'humidity': 1.0,         # Important for comfort index
        'pressure': 1.0          # Key for weather system predictions
    }
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss={
            col: losses.Huber() if col in ['temperature_max', 'pressure'] 
            else losses.LogCosh() if col in ['rainfall', 'snowfall']
            else losses.MSE() for col in TARGET_COLS
        },
        loss_weights=[loss_weights[col] for col in TARGET_COLS],
        metrics=['mae']
    )
    
    return model

# Main workflow
def main():
    # Load and preprocess data
    df = pd.read_csv("dataset.csv", parse_dates=['date'])
    preprocessor = WeatherPreprocessor(TARGET_COLS)
    processed_df = preprocessor.create_features(df)
    
    # Split data
    split_idx = int(len(processed_df) * 0.8)
    train_df = processed_df.iloc[:split_idx]
    test_df = processed_df.iloc[split_idx:]
    
    X_train, y_train = preprocessor.fit_transform(
        train_df.drop(columns=TARGET_COLS + ['date']), 
        train_df[TARGET_COLS]
    )
    X_test, y_test = preprocessor.transform(
        test_df.drop(columns=TARGET_COLS + ['date']), 
        test_df[TARGET_COLS]
    )
    
    # Save preprocessing objects
    joblib.dump(preprocessor, SCALER_SAVE_PATH)
    
    # Build and train model
    model = build_multi_target_model(X_train.shape[1], len(TARGET_COLS))
    
    callbacks = [
        keras.callbacks.EarlyStopping(patience=20, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
    ]
    
    history = model.fit(
        X_train, [y_train[:,i] for i in range(y_train.shape[1])],
        epochs=300,
        batch_size=64,
        validation_split=0.15,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    y_preds = model.predict(X_test)
    y_test = preprocessor.inverse_transform(y_test)
    y_pred = preprocessor.inverse_transform(y_preds)
    
    # Generate comprehensive metrics
    results = {}
    for i, col in enumerate(TARGET_COLS):
        results[col] = {
            'MAE': mean_absolute_error(y_test[i], y_pred[i]),
            'RMSE': np.sqrt(mean_squared_error(y_test[i], y_pred[i])),
            'R²': r2_score(y_test[i], y_pred[i]),
        }
        
        # Special metrics for precipitation
        if 'rain' in col.lower() or 'snow' in col.lower():
            y_true_bin = (y_test[i] > 0.1).astype(int)
            y_pred_bin = (y_pred[i] > 0.1).astype(int)
            results[col].update({
                'F1': f1_score(y_true_bin, y_pred_bin),
                'Precision': precision_score(y_true_bin, y_pred_bin),
                'Recall': recall_score(y_true_bin, y_pred_bin),
            })
    
    # Print results
    print("\n✅ Final Evaluation Results:")
    for col, metrics in results.items():
        print(f"\n📊 {col}:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

    # Visualizations
    plt.figure(figsize=(15, 20))
    for i, col in enumerate(TARGET_COLS):
        plt.subplot(len(TARGET_COLS), 1, i+1)
        plt.plot(y_test[i][:100], label='True')
        plt.plot(y_pred[i][:100], label='Predicted', alpha=0.7)
        plt.title(col)
        plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()