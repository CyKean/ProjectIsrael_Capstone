# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow import keras

# # Load preprocessing artifacts and model
# selected_feature_names = np.load('preprocessing/selected_feature_names.npy', allow_pickle=True)
# power_transformer = np.load('preprocessing/power_transformer.npy', allow_pickle=True).item()
# robust_scaler = np.load('preprocessing/robust_scaler.npy', allow_pickle=True).item()
# label_classes = np.load('preprocessing/label_classes.npy', allow_pickle=True)
# model = keras.models.load_model('crop_model.keras')

# def create_interaction_features(X):
#     """Recreate the same feature engineering as in training"""
#     numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
#     for i in range(len(numeric_cols)):
#         for j in range(i+1, len(numeric_cols)):
#             col1, col2 = numeric_cols[i], numeric_cols[j]
#             X[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-6)
#             X[f'{col1}_{col2}_product'] = X[col1] * X[col2]
#     return X

# def preprocess_input(data):
#     """Replicate the preprocessing pipeline from training"""
#     # Feature engineering
#     processed = create_interaction_features(data.copy())
    
#     # Handle categorical data (if any)
#     categorical_cols = processed.select_dtypes(include=['object']).columns
#     processed = pd.get_dummies(processed, columns=categorical_cols)
    
#     # Ensure all required features are present
#     for feature in selected_feature_names:
#         if feature not in processed.columns:
#             processed[feature] = 0
            
#     # Select and order features exactly like training
#     processed = processed[selected_feature_names]
    
#     # Handle infinite/NaN values
#     processed = processed.replace([np.inf, -np.inf], np.nan).fillna(0)
    
#     # Apply transformations
#     transformed = power_transformer.transform(processed)
#     scaled = robust_scaler.transform(transformed)
    
#     return scaled


# test_data = {
#     'N (ppm)': [177.3236749791357],
#     'P (ppm)': [59.3828625804493],
#     'K (ppm)': [128.66729314027663],
#     'Temp (°C)': [22.45599180994067],
#     'Humidity (%)': [76.16831418735637],
#     'pH': [6.146048236304035],
#     'Rainfall (mm/month)': [166.4953071940234],
#     'Wind Speed (m/s)': [0.1778431699078139],
#     'Pressure (hPa)': [990.4208747001574],
#     'Cloud Cover (%)': [62.97573573961281],
#     'NPK Ratio': [5.067513447407936],
#     'Soil Fertility Index': [127.34451670787206],
#     'Soil Moisture (%)': [33.79723181882302]
# }


# # Convert to DataFrame
# test_df = pd.DataFrame(test_data)

# # Preprocess the input
# processed_input = preprocess_input(test_df)

# # Make prediction
# prediction = model.predict(processed_input)
# probabilities = prediction[0]

# # Get top 3 predictions
# top3_indices = np.argsort(probabilities)[-3:][::-1]
# top3_crops = [(label_classes[i], probabilities[i]) for i in top3_indices]

# # Display results
# print("\nTest Data Input:")
# print(test_df.T)
# print("\nPreprocessed Shape:", processed_input.shape)
# print("\nTop 3 Predicted Crops:")
# for rank, (crop, prob) in enumerate(top3_crops, 1):
#     print(f"{rank}. {crop}: {prob:.4f} ({prob*100:.2f}%)")


import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

# Load preprocessing artifacts and model
selected_feature_names = np.load('preprocessing/selected_feature_names.npy', allow_pickle=True)
power_transformer = np.load('preprocessing/power_transformer.npy', allow_pickle=True).item()
robust_scaler = np.load('preprocessing/robust_scaler.npy', allow_pickle=True).item()
label_classes = np.load('preprocessing/label_classes.npy', allow_pickle=True)
model = keras.models.load_model('crop_model.keras')

# Load dataset for reference (adjust the filename accordingly)
dataset = pd.read_csv("crop_dataset_fixed.csv")  # The dataset used for training

def get_optimal_soil_values(crop_name, dataset):
    """Get the average soil values for a given crop from the dataset."""
    crop_data = dataset[dataset['Crop'] == crop_name]
    if crop_data.empty:
        return None  # No data for this crop

    return crop_data[['N (ppm)', 'P (ppm)', 'K (ppm)', 'NPK Ratio', 'Soil Fertility Index', 'Soil Moisture (%)']].mean().to_dict()

def create_interaction_features(X):
    """Recreate the same feature engineering as in training"""
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            X[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-6)
            X[f'{col1}_{col2}_product'] = X[col1] * X[col2]
    return X

def preprocess_input(data):
    """Replicate the preprocessing pipeline from training"""
    processed = create_interaction_features(data.copy())
    
    categorical_cols = processed.select_dtypes(include=['object']).columns
    processed = pd.get_dummies(processed, columns=categorical_cols)
    
    for feature in selected_feature_names:
        if feature not in processed.columns:
            processed[feature] = 0
            
    processed = processed[selected_feature_names]
    
    processed = processed.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    transformed = power_transformer.transform(processed)
    scaled = robust_scaler.transform(transformed)
    
    return scaled

# Sample test data
# test_data = {
#     'N (ppm)': [160.45901534408546],
#     'P (ppm)': [63.99842502861839],
#     'K (ppm)': [178.77649487432782],
#     'Temp (°C)': [24.96442467685059],
#     'Humidity (%)': [80.30622987909408],
#     'pH': [6.780095135993347],
#     'Rainfall (mm/month)': [164.14623220579836],
#     'Wind Speed (m/s)': [0.15265208732575197],
#     'Pressure (hPa)': [1016.5234968854118],
#     'Cloud Cover (%)': [50.83306451494143],
#     'NPK Ratio': [5.219134310855226],
#     'Soil Fertility Index': [137.01608210851805],
#     'Soil Moisture (%)': [35.4054165957536]
# }

# test_data = {
#     'N (ppm)': [177.32],
#     'P (ppm)': [59.38],
#     'K (ppm)': [128.67],
#     'Temp (°C)': [22.45],
#     'Humidity (%)': [76.16],
#     'pH': [6.14],
#     'Rainfall (mm/month)': [166.49],
#     'Wind Speed (m/s)': [0.17],
#     'Pressure (hPa)': [990.42],
#     'Cloud Cover (%)': [62.97],
#     'NPK Ratio': [5.06],
#     'Soil Fertility Index': [127.34],
#     'Soil Moisture (%)': [33.79]
# }

# test_data = {
#     'N (ppm)': [50],
#     'P (ppm)': [30],
#     'K (ppm)': [40],
#     'Temp (°C)': [25],
#     'Humidity (%)': [70],
#     'pH': [6.5],
#     'Rainfall (mm/month)': [150],
#     'Wind Speed (m/s)': [3],
#     'Pressure (hPa)': [1013],
#     'Cloud Cover (%)': [50],
#     'NPK Ratio': [1.2],
#     'Soil Fertility Index': [0.8],
#     'Soil Moisture (%)': [60]
# }


test_data = {
    'N (ppm)': [143.82921691918315],
    'P (ppm)': [43.19672500242768],
    'K (ppm)': [135.41607186470273],
    'Temp (°C)': [20.204552927810507],
    'Humidity (%)': [77.6387728473247],
    'pH': [6.4312535187036115],
    'Rainfall (mm/month)': [109.56013972138203],
    'Wind Speed (m/s)': [0.7395617216168717],
    'Pressure (hPa)': [1002.3395807545214],
    'Cloud Cover (%)': [49.2907301974442],
    'NPK Ratio': [6.318234863975719],
    'Soil Fertility Index': [111.11552582781239],
    'Soil Moisture (%)': [33.246711933357524]
}


test_df = pd.DataFrame(test_data)

# Preprocess the input
processed_input = preprocess_input(test_df)

# Make prediction
prediction = model.predict(processed_input)
probabilities = prediction[0]

# Get top 3 predictions
top3_indices = np.argsort(probabilities)[-3:][::-1]
top3_crops = [(label_classes[i], probabilities[i]) for i in top3_indices]

# Display results
print("\nTest Data Input:")
print(test_df.T)
print("\nPreprocessed Shape:", processed_input.shape)
print("\nTop 3 Predicted Crops:")
for rank, (crop, prob) in enumerate(top3_crops, 1):
    print(f"{rank}. {crop}: {prob:.4f} ({prob*100:.2f}%)")

# Check if top-1 probability is lower than 75%
top1_crop, top1_prob = top3_crops[0]
if top1_prob < 0.75:
    print(f"\n⚠️ Confidence is low ({top1_prob * 100:.2f}%). Consider improving soil conditions.")

    # Get optimal soil values for this crop
    optimal_values = get_optimal_soil_values(top1_crop, dataset)

    if optimal_values:
        print("🔍 Suggested Soil Adjustments:")
        for feature, ideal_value in optimal_values.items():
            current_value = test_df[feature].values[0]
            if abs(current_value - ideal_value) > 10:  # Significant deviation threshold
                print(f"   - Adjust {feature}: Current = {current_value:.2f}, Recommended = {ideal_value:.2f}")
    else:
        print("⚠️ No reference data available for this crop.")
