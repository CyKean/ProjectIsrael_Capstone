import pandas as pd
import numpy as np
import joblib
import os
import tensorflow as tf
from tensorflow import keras

class CropPredictor:
    def __init__(self, model_dir='models', preprocessing_dir='preprocessing'):
        """Initialize the crop predictor with saved models and preprocessors."""
        self.model_dir = model_dir
        self.preprocessing_dir = preprocessing_dir
        self.load_components()
    
    def load_components(self):
        """Load all necessary components for prediction."""
        # Load preprocessing components
        self.power_transformer = joblib.load(
            os.path.join(self.preprocessing_dir, 'power_transformer.joblib'))
        self.robust_scaler = joblib.load(
            os.path.join(self.preprocessing_dir, 'robust_scaler.joblib'))
        self.selected_feature_names = np.load(
            os.path.join(self.preprocessing_dir, 'selected_feature_names.npy'), 
            allow_pickle=True).tolist()
        self.label_classes = np.load(
            os.path.join(self.preprocessing_dir, 'label_classes.npy'), 
            allow_pickle=True)
        
        # Load models
        self.nn_model = keras.models.load_model(
            os.path.join(self.model_dir, 'crop_nn_model.keras'))
        
        self.xgb_model = None
        xgb_path = os.path.join(self.model_dir, 'crop_xgb_model.joblib')
        if os.path.exists(xgb_path):
            try:
                self.xgb_model = joblib.load(xgb_path)
            except Exception as e:
                print(f"Warning: Could not load XGBoost model: {e}")
        
        # Determine best model
        self.best_model_type = 'nn'  # default
        best_model_path = os.path.join(self.model_dir, 'best_model.txt')
        if os.path.exists(best_model_path):
            with open(best_model_path, 'r') as f:
                self.best_model_type = f.read().strip()
    
    def create_interaction_features(self, df_X):
        """Create interaction features (must match training)."""
        numeric_cols = df_X.select_dtypes(include=[np.number]).columns.tolist()
        X_eng = df_X.copy()
        
        interaction_count = 0
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                col1, col2 = numeric_cols[i], numeric_cols[j]
                X_eng[f'{col1}_div_{col2}'] = X_eng[col1] / (X_eng[col2] + 1e-8)
                X_eng[f'{col1}_x_{col2}'] = X_eng[col1] * X_eng[col2]
                X_eng[f'{col1}_plus_{col2}'] = X_eng[col1] + X_eng[col2]
                X_eng[f'{col1}_minus_{col2}'] = X_eng[col1] - X_eng[col2]
                
                if interaction_count < 10:
                    X_eng[f'{col1}_squared'] = X_eng[col1] ** 2
                    X_eng[f'{col2}_squared'] = X_eng[col2] ** 2
                
                interaction_count += 4
        
        return X_eng
    
    def predict(self, features_dict, return_probabilities=False):
        """
        Make crop predictions from input features.
        
        Args:
            features_dict: Dictionary with feature names as keys
            return_probabilities: Whether to return class probabilities
            
        Returns:
            Dictionary with prediction results
        """
        # Convert to DataFrame
        input_df = pd.DataFrame([features_dict])
        
        # Feature engineering
        input_df_eng = self.create_interaction_features(input_df)
        input_df_eng = pd.get_dummies(input_df_eng, dummy_na=False, drop_first=True)
        
        # Align features with training
        for feature in self.selected_feature_names:
            if feature not in input_df_eng.columns:
                input_df_eng[feature] = 0
        
        input_df_selected = input_df_eng[self.selected_feature_names]
        
        # Preprocessing
        input_df_selected = input_df_selected.replace([np.inf, -np.inf], np.nan).fillna(0)
        input_power = self.power_transformer.transform(input_df_selected)
        input_scaled = self.robust_scaler.transform(input_power)
        
        # Make predictions
        if self.best_model_type == 'nn':
            probabilities = self.nn_model.predict(input_scaled, verbose=0)[0]
        elif self.best_model_type == 'xgb' and self.xgb_model is not None:
            probabilities = self.xgb_model.predict_proba(input_scaled)[0]
        elif self.best_model_type == 'ensemble' and self.xgb_model is not None:
            nn_probs = self.nn_model.predict(input_scaled, verbose=0)[0]
            xgb_probs = self.xgb_model.predict_proba(input_scaled)[0]
            probabilities = 0.6 * nn_probs + 0.4 * xgb_probs
        else:
            # Fallback to NN
            probabilities = self.nn_model.predict(input_scaled, verbose=0)[0]
        
        predicted_class_idx = np.argmax(probabilities)
        predicted_class = self.label_classes[predicted_class_idx]
        confidence = probabilities[predicted_class_idx]
        
        result = {
            'predicted_crop': predicted_class,
            'confidence': float(confidence),
            'top_3_predictions': []
        }
        
        # Add top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        for idx in top_3_indices:
            result['top_3_predictions'].append({
                'crop': self.label_classes[idx],
                'probability': float(probabilities[idx])
            })
        
        if return_probabilities:
            result['all_probabilities'] = {
                self.label_classes[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
        
        return result

# Example usage:
# predictor = CropPredictor()
# features = {'N': 90, 'P': 42, 'K': 43, 'temperature': 20.9, 'humidity': 82.0, 'ph': 6.5, 'rainfall': 202.9}
# prediction = predictor.predict(features)
# print(f"Recommended crop: {prediction['predicted_crop']}")
# print(f"Confidence: {prediction['confidence']:.2%}")
