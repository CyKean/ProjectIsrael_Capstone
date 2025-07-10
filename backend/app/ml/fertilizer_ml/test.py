# import joblib
# import numpy as np
# import pandas as pd
# from pathlib import Path

# def load_models():
#     """Load all trained models and encoders"""
#     try:
#         # Get the directory where this file is located
#         current_dir = Path(__file__).parent
        
#         # Load models using absolute paths
#         type_model = joblib.load(current_dir / "fertilizer_type_classifier.pkl")
#         name_model = joblib.load(current_dir / "fertilizer_name_classifier.pkl")
#         amount_model = joblib.load(current_dir / "fertilizer_amount_regressor.pkl")
#         type_encoder = joblib.load(current_dir / "fertilizer_type_encoder.pkl")
#         name_encoder = joblib.load(current_dir / "fertilizer_name_encoder.pkl")
        
#         print("✅ All models loaded successfully!")
#         return type_model, name_model, amount_model, type_encoder, name_encoder
#     except Exception as e:
#         print(f"❌ Error loading models: {str(e)}")
#         return None

# def predict_fertilizer(soil_data, models):
#     try:
#         # Unpack models
#         type_model = models['type_model']
#         name_model = models['name_model']
#         amount_model = models['amount_model']
#         type_encoder = models['type_encoder']
#         name_encoder = models['name_encoder']
        
#         # Create feature vector
#         features = np.array([[soil_data['N'], soil_data['P'], soil_data['K'], soil_data['pH'], soil_data['OM']]])
        
#         # Predict fertilizer type
#         fertilizer_type_encoded = type_model.predict(features)[0]
#         fertilizer_type = type_encoder.inverse_transform([fertilizer_type_encoded])[0]
        
#         # Predict fertilizer name
#         fertilizer_name_encoded = name_model.predict(features)[0]
#         fertilizer_name = name_encoder.inverse_transform([fertilizer_name_encoded])[0]
        
#         # Predict amount
#         amount = amount_model.predict(features)[0]
        
#         return {
#             'type': fertilizer_type,
#             'name': fertilizer_name,
#             'amount': round(float(amount), 2)  # ensure it's JSON serializable
#         }

#     except Exception as e:
#         print(f"❌ Fertilizer prediction failed: {e}")
#         raise ValueError("Fertilizer prediction failed") from e

# def main():
#     # Load models
#     models = load_models()
#     if models is None:
#         return
    
#     # Test cases
#     test_cases = [
#         {
#             'name': "Low Nutrient Soil",
#             'data': {'N': 10, 'P': 5, 'K': 30, 'pH': 6.5, 'OM': 1.0}
#         },
#         {
#             'name': "Medium Nutrient Soil",
#             'data': {'N': 30, 'P': 15, 'K': 60, 'pH': 7.0, 'OM': 2.5}
#         },
#         {
#             'name': "High Nutrient Soil",
#             'data': {'N': 50, 'P': 30, 'K': 100, 'pH': 7.5, 'OM': 4.0}
#         },
#         {
#             'name': "Acidic Soil",
#             'data': {'N': 20, 'P': 10, 'K': 40, 'pH': 5.0, 'OM': 2.0}
#         },
#         {
#             'name': "Alkaline Soil",
#             'data': {'N': 25, 'P': 20, 'K': 70, 'pH': 8.0, 'OM': 3.0}
#         }
#     ]
    
#     # Run predictions
#     print("\n🌱 Testing Fertilizer Recommendations:")
#     print("-" * 50)
    
#     for test_case in test_cases:
#         print(f"\nTest Case: {test_case['name']}")
#         print("Soil Conditions:")
#         for key, value in test_case['data'].items():
#             print(f"  {key}: {value}")
        
#         result = predict_fertilizer(test_case['data'], models)
        
#         print("\nRecommendation:")
#         print(f"  Fertilizer Type: {result['type']}")
#         print(f"  Fertilizer Name: {result['name']}")
#         print(f"  Amount: {result['amount']} units per square meter")
#         print("-" * 50)

# if __name__ == "__main__":
#     main()


import joblib
import numpy as np
import pandas as pd
from pathlib import Path

def load_models():
    """Load all trained models and encoders into a dictionary"""
    try:
        current_dir = Path(__file__).parent

        models = {
            'type_model': joblib.load(current_dir / "fertilizer_type_classifier.pkl"),
            'name_model': joblib.load(current_dir / "fertilizer_name_classifier.pkl"),
            'amount_model': joblib.load(current_dir / "fertilizer_amount_regressor.pkl"),
            'type_encoder': joblib.load(current_dir / "fertilizer_type_encoder.pkl"),
            'name_encoder': joblib.load(current_dir / "fertilizer_name_encoder.pkl")
        }

        print("✅ All models loaded successfully!")
        return models
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        return None

def predict_fertilizer(soil_data, models):
    try:
        # Unpack models
        type_model = models['type_model']
        name_model = models['name_model']
        amount_model = models['amount_model']
        type_encoder = models['type_encoder']
        name_encoder = models['name_encoder']

        # Create DataFrame input with column names expected by the trained model
            # The keys in soil_data are 'N', 'P', 'K', 'pH', 'OM', 'Crop Type'
        # The model expects "Nitrogen (mg/kg)", "Phosphorus (mg/kg)", etc.
        features_for_df = {
            "Nitrogen (mg/kg)": [soil_data['N']],
            "Phosphorus (mg/kg)": [soil_data['P']],
            "Potassium (mg/kg)": [soil_data['K']],
            "pH": [soil_data['pH']],
                "Organic Matter (%)": [soil_data['OM']],
                "Crop Type": [soil_data['Crop Type']] # Added Crop Type
        }
        features = pd.DataFrame(features_for_df)

        # Predict fertilizer type
        fertilizer_type_encoded = type_model.predict(features)[0]
        fertilizer_type = type_encoder.inverse_transform([fertilizer_type_encoded])[0]

        # Predict fertilizer name
        fertilizer_name_encoded = name_model.predict(features)[0]
        fertilizer_name = name_encoder.inverse_transform([fertilizer_name_encoded])[0]

        # Predict amount
        amount = amount_model.predict(features)[0]

        return {
            'type': fertilizer_type,
            'name': fertilizer_name,
            'amount': round(float(amount), 2)
        }

    except Exception as e:
        print(f"❌ Fertilizer prediction failed: {e}")
        raise ValueError("Fertilizer prediction failed") from e

def main():
    models = load_models()
    if models is None:
        return

    test_cases = [
        {
            'name': "Low Nutrient Soil",
            'data': {'N': 10, 'P': 5, 'K': 30, 'pH': 6.5, 'OM': 1.0, 'Crop Type': 'Rice'} # Added default Crop Type
        },
        {
            'name': "Medium Nutrient Soil",
            'data': {'N': 30, 'P': 15, 'K': 60, 'pH': 7.0, 'OM': 2.5, 'Crop Type': 'Corn'} # Added default Crop Type
        },
        {
            'name': "High Nutrient Soil",
            'data': {'N': 50, 'P': 30, 'K': 100, 'pH': 7.5, 'OM': 4.0, 'Crop Type': 'Vegetables'} # Added default Crop Type
        },
        {
            'name': "Acidic Soil",
            'data': {'N': 20, 'P': 10, 'K': 40, 'pH': 5.0, 'OM': 2.0, 'Crop Type': 'Fruits'} # Added default Crop Type
        },
        {
            'name': "Alkaline Soil",
            'data': {'N': 25, 'P': 20, 'K': 70, 'pH': 8.0, 'OM': 3.0, 'Crop Type': 'Rice'} # Added default Crop Type
        }
    ]

    print("\n🌱 Testing Fertilizer Recommendations:")
    print("-" * 50)

    for test_case in test_cases:
        print(f"\nTest Case: {test_case['name']}")
        print("Soil Conditions:")
        for key, value in test_case['data'].items():
            print(f"  {key}: {value}")

        try:
            result = predict_fertilizer(test_case['data'], models)
            print("\nRecommendation:")
            print(f"  Fertilizer Type: {result['type']}")
            print(f"  Fertilizer Name: {result['name']}")
            print(f"  Amount: {result['amount']} units per square meter")
        except Exception as e:
            print(f"  ❌ Error during prediction: {e}")
        print("-" * 50)

if __name__ == "__main__":
    main()
