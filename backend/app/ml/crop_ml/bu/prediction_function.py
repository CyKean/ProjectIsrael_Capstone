
import pandas as pd
import numpy as np
import joblib
import os
import tensorflow as tf
from tensorflow import keras

# Load preprocessing objects
power_transformer = joblib.load('preprocessing/power_transformer.joblib')
robust_scaler = joblib.load('preprocessing/robust_scaler.joblib')
selected_feature_names = np.load('preprocessing/selected_feature_names.npy', allow_pickle=True)
label_classes = np.load('preprocessing/label_classes.npy')

# Load models
nn_model = keras.models.load_model('crop_nn_model.keras')
try:
    xgb_model = joblib.load('crop_xgb_model.joblib')
    have_xgb = True
except:
    have_xgb = False

# Read best model type
with open('best_model.txt', 'r') as f:
    best_model_type = f.read().strip()

def predict_crop(features_dict):
    """
    Make a prediction for crop recommendation based on soil and weather features.
    
    Args:
        features_dict: Dictionary with keys for N, P, K, Temp, Humidity, pH, Soil Moisture
        
    Returns:
        Predicted crop name and probability
    """
    # Convert input to DataFrame
    input_df = pd.DataFrame([features_dict])
    
    # Create interaction features
    for i, col1 in enumerate(['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)']):
        for j, col2 in enumerate(['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)'])[i+1:]:
            if col1 in input_df.columns and col2 in input_df.columns:
                input_df[f'{col1}_{col2}_ratio'] = input_df[col1] / (input_df[col2] + 1e-6)
                input_df[f'{col1}_{col2}_product'] = input_df[col1] * input_df[col2]
    
    # One-hot encode any categorical features (if any)
    input_df = pd.get_dummies(input_df)
    
    # Ensure all selected features are present
    for feature in selected_feature_names:
        if feature not in input_df.columns:
            input_df[feature] = 0
    
    # Select only the features used in training
    input_df = input_df[selected_feature_names]
    
    # Apply transformations
    input_transformed = power_transformer.transform(input_df)
    input_scaled = robust_scaler.transform(input_transformed)
    
    # Get predictions
    if best_model_type == "nn" or not have_xgb:
        probabilities = nn_model.predict(input_scaled)[0]
        predicted_class_idx = np.argmax(probabilities)
        confidence = probabilities[predicted_class_idx]
    elif best_model_type == "xgb":
        probabilities = xgb_model.predict_proba(input_scaled)[0]
        predicted_class_idx = np.argmax(probabilities)
        confidence = probabilities[predicted_class_idx]
    else:  # ensemble
        nn_probs = nn_model.predict(input_scaled)[0]
        xgb_probs = xgb_model.predict_proba(input_scaled)[0]
        probabilities = (nn_probs + xgb_probs) / 2
        predicted_class_idx = np.argmax(probabilities)
        confidence = probabilities[predicted_class_idx]
    
    # Convert back to original crop name
    predicted_crop = label_classes[predicted_class_idx]
    
    return {
        'crop': predicted_crop,
        'confidence': float(confidence),
        'class_idx': int(predicted_class_idx)
    }
