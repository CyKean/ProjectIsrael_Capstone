
import pandas as pd
import numpy as np
import joblib
import os
import tensorflow as tf
from tensorflow import keras # Required for custom layers like LeakyReLU if used directly

# --- Define Paths ---
SCRIPT_DIR = os.path.dirname(__file__) # Assumes script is run from its location
PREPROCESSING_DIR_PRED = os.path.join(SCRIPT_DIR, 'preprocessing')
MODELS_DIR_PRED = os.path.join(SCRIPT_DIR, 'models')

power_transformer = joblib.load(os.path.join(PREPROCESSING_DIR_PRED, 'power_transformer.joblib'))
robust_scaler = joblib.load(os.path.join(PREPROCESSING_DIR_PRED, 'robust_scaler.joblib'))
selected_feature_names = np.load(os.path.join(PREPROCESSING_DIR_PRED, 'selected_feature_names.npy'), allow_pickle=True).tolist()
label_encoder_classes = np.load(os.path.join(PREPROCESSING_DIR_PRED, 'label_classes.npy'), allow_pickle=True)

nn_model_path = os.path.join(MODELS_DIR_PRED, 'crop_nn_model.keras')
xgb_model_path = os.path.join(MODELS_DIR_PRED, 'crop_xgb_model.joblib')
best_model_type_path = os.path.join(MODELS_DIR_PRED, 'best_model.txt')

nn_model = keras.models.load_model(nn_model_path)
xgb_model = None
have_xgb = False
if os.path.exists(xgb_model_path):
    try:
        xgb_model = joblib.load(xgb_model_path)
        have_xgb = True
    except Exception as e:
        print(f"Warning: Could not load XGBoost model: {e}")

best_model_type = "nn" # Default
if os.path.exists(best_model_type_path):
    with open(best_model_type_path, 'r') as f:
        best_model_type = f.read().strip()
else:
    print(f"Warning: best_model.txt not found. Defaulting to NN model for predictions.")


# --- Feature Engineering Function (must match training) ---
def create_interaction_features(df_X):
    numeric_cols = df_X.select_dtypes(include=np.number).columns.tolist()
    X_eng = df_X.copy()
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            X_eng[f'{col1}_div_{col2}'] = X_eng[col1] / (X_eng[col2] + 1e-6)
            X_eng[f'{col1}_x_{col2}'] = X_eng[col1] * X_eng[col2]
            X_eng[f'{col1}_plus_{col2}'] = X_eng[col1] + X_eng[col2]
            X_eng[f'{col1}_minus_{col2}'] = X_eng[col1] - X_eng[col2]
    return X_eng

# --- Prediction Function ---
def predict_crop(features_dict):
    """
    Make a prediction for crop recommendation.
    
    Args:
        features_dict: Dictionary with keys for ['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)']
        
    Returns:
        Dictionary with 'crop', 'confidence', and 'all_crop_probabilities'
    """
    input_df = pd.DataFrame([features_dict])
    
    # 1. Feature Engineering (must be identical to training)
    input_df_eng = create_interaction_features(input_df)
    
    # 2. Handle Categoricals (if any new ones were created, though unlikely with numeric inputs)
    input_df_eng = pd.get_dummies(input_df_eng, dummy_na=False)
    
    # 3. Align features with training (add missing, reorder, and select)
    # Add missing columns with 0 (features model was trained on but not in input)
    for feature in selected_feature_names:
        if feature not in input_df_eng.columns:
            input_df_eng[feature] = 0
    # Ensure correct order and selection of features
    input_df_selected = input_df_eng[selected_feature_names]
            
    # 4. Preprocessing (transform, scale)
    input_df_selected = input_df_selected.replace([np.inf, -np.inf], np.nan)
    # Fill NaNs based on training strategy (e.g., with 0 or median if that was used)
    # For safety, let's fill with 0 if any NaNs remain after engineering/selection.
    # A more robust way would be to save medians from training if used for filling.
    if input_df_selected.isna().any().any():
        input_df_selected = input_df_selected.fillna(0) 

    input_power = power_transformer.transform(input_df_selected)
    input_robust = robust_scaler.transform(input_power)
    
    # 5. Prediction
    if best_model_type == "ensemble" and have_xgb:
        nn_probs_single = nn_model.predict(input_robust)[0]
        xgb_probs_single = xgb_model.predict_proba(input_robust)[0]
        # Ensure consistent shape if num_classes differs slightly (should not happen with proper setup)
        # This is a safeguard; ideally, both models output probs for all original classes.
        if len(nn_probs_single) != len(xgb_probs_single):
             # Fallback or error handling needed if class counts are inconsistent - added print warning
             # For now, let's assume nn_model has the definitive class count
             if len(nn_probs_single) > len(xgb_probs_single):
                 padded_xgb_probs = np.zeros(len(nn_probs_single))
                 padded_xgb_probs[:len(xgb_probs_single)] = xgb_probs_single
                 xgb_probs_single = padded_xgb_probs
             else: # xgb_probs_single is longer, truncate or pad nn_probs
                 padded_nn_probs = np.zeros(len(xgb_probs_single))
                 padded_nn_probs[:len(nn_probs_single)] = nn_probs_single
                 nn_probs_single = padded_nn_probs
             print(f"Warning: NN and XGBoost models have inconsistent output shapes (NN: {len(nn_probs_single)}, XGB: {len(xgb_probs_single)}). Attempting to align for ensemble.")
             # A more robust solution might involve re-training one of the models or aligning classes explicitly.
        probabilities = (0.5 * nn_probs_single + 0.5 * xgb_probs_single) # Consistent 0.5/0.5 weights
    elif best_model_type == "xgb" and have_xgb:
        probabilities = xgb_model.predict_proba(input_robust)[0]
    else: # Default to NN or if XGB failed/not chosen
        probabilities = nn_model.predict(input_robust)[0]
        
    predicted_class_idx = np.argmax(probabilities)
    confidence = float(probabilities[predicted_class_idx])
    predicted_crop = label_encoder_classes[predicted_class_idx]

    all_crop_probabilities = {
        label_encoder_classes[i]: float(probabilities[i]) 
        for i in range(len(probabilities))
    }
    
    return {
        'crop': predicted_crop,
        'confidence': confidence,
        'class_idx': int(predicted_class_idx),
        'all_crop_probabilities': all_crop_probabilities
    }

if __name__ == '__main__':
    # Example usage:
    # Ensure your feature names match exactly those in 'original_feature_names_list'
    # These are the features BEFORE any engineering.
    example_features = {
        'N (ppm)': 100, 
        'P (ppm)': 50, 
        'K (ppm)': 50, 
        # Add more features as per your original dataset
        # 'Temp (°C)': 25, 
        # 'Humidity (%)': 70, 
        # 'pH': 6.5, 
        # 'Soil Moisture (%)': 60
    }
    # Fill remaining original features with a default value (e.g., 0 or mean) if not provided in the example
    all_original_features = ['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)']
    for feat_name in all_original_features:
        if feat_name not in example_features:
            example_features[feat_name] = 0 # Or a typical/mean value

    prediction = predict_crop(example_features)
    print(f"Example Prediction:")
    print(f"  Predicted Crop: {prediction.get('crop', 'N/A')}")
    print(f"  Confidence: {prediction.get('confidence', 0.0):.4f}")
    # print(f"  All Probabilities: {prediction.get('all_crop_probabilities', {})}")

