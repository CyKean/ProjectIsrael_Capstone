# import os
# import sys
# from pathlib import Path
# from app.ml.crop_ml.prediction_function import predict_crop
# from app.ml.fertilizer_ml.test import load_models, predict_fertilizer

# def check_models_exist():
#     """Check if all required model files exist"""
#     base_path = Path(__file__).parent / "fertilizer_ml"
#     required_files = [
#         "fertilizer_type_classifier.pkl",
#         "fertilizer_name_classifier.pkl",
#         "fertilizer_amount_regressor.pkl",
#         "fertilizer_type_encoder.pkl",
#         "fertilizer_name_encoder.pkl"
#     ]
    
#     missing_files = []
#     for file in required_files:
#         if not (base_path / file).exists():
#             missing_files.append(file)
    
#     return missing_files

# def get_integrated_recommendation(soil_data):
#     """
#     Get integrated crop and fertilizer recommendations
    
#     Args:
#         soil_data: dict with keys:
#             - 'N (ppm)': Nitrogen content
#             - 'P (ppm)': Phosphorus content
#             - 'K (ppm)': Potassium content
#             - 'Temp (°C)': Temperature
#             - 'Humidity (%)': Humidity
#             - 'pH': pH level
#             - 'Soil Moisture (%)': Soil moisture
    
#     Returns:
#         dict containing crop recommendations and fertilizer recommendations for each crop
#     """
#     try:
#         # Check if models exist
#         missing_files = check_models_exist()
#         if missing_files:
#             return {
#                 "error": "Missing model files",
#                 "details": f"Please train the fertilizer models first. Missing files: {', '.join(missing_files)}",
#                 "soil_conditions": soil_data
#             }
        
#         # Get crop recommendations
#         crop_recommendations = predict_crop(soil_data, top_k=3)
        
#         # Load fertilizer models
#         fertilizer_models = load_models()
#         if fertilizer_models is None:
#             return {
#                 "error": "Failed to load fertilizer models",
#                 "details": "Error loading the trained models. Please ensure models are properly trained.",
#                 "soil_conditions": soil_data
#             }
        
    
    
#         # Convert ppm to mg/kg (1 ppm = 1 mg/kg)
#         fertilizer_soil_data = {
#             'N': soil_data['N (ppm)'],
#             'P': soil_data['P (ppm)'],
#             'K': soil_data['K (ppm)'],
#             'pH': soil_data['pH'],
#             'OM': 2.0  # Default value, should be provided in actual data
#         }
        
#         # Get fertilizer recommendations for each crop
#         recommendations = {
#             "soil_conditions": soil_data,
#             "recommendations": []
#         }
        
#         for crop_rec in crop_recommendations:
#             fertilizer_rec = predict_fertilizer(fertilizer_soil_data, fertilizer_models)
            
#             # Calculate adjusted amount based on crop confidence
#             base_amount = fertilizer_rec['amount']
#             confidence = crop_rec['confidence']
#             adjusted_amount = base_amount * (0.5 + 0.5 * confidence)  # Scale amount by confidence
            
#             recommendation = {
#                 "crop": crop_rec['crop'],
#                 "confidence": crop_rec['confidence'],
#                 "fertilizer": {
#                     "type": fertilizer_rec['type'],
#                     "name": fertilizer_rec['name'],
#                     "base_amount": base_amount,
#                     "adjusted_amount": round(adjusted_amount, 2),
#                     "unit": "kg/m²" if fertilizer_rec['type'] == 'solid' else 'L/m²'
#                 }
#             }
            
#             # Add additional metrics if available
#             if 'soilCompatibility' in crop_rec:
#                 recommendation.update({
#                     "soil_compatibility": crop_rec['soilCompatibility'],
#                     "growth_rate": crop_rec['growthRate'],
#                     "yield_potential": crop_rec['yieldPotential']
#                 })
            
#             recommendations["recommendations"].append(recommendation)
        
#         return recommendations
    
#     except Exception as e:
#         return {
#             "error": "Unexpected error",
#             "details": str(e),
#             "soil_conditions": soil_data
#         }

# def print_recommendations(result):
#     """Pretty print the recommendations"""
#     print("\n🌱 Integrated Crop and Fertilizer Recommendations")
#     print("-" * 60)
    
#     # Print soil conditions
#     print("\nSoil Conditions:")
#     for key, value in result["soil_conditions"].items():
#         print(f"  {key}: {value}")
    
#     # Check for errors
#     if "error" in result:
#         print(f"\n❌ Error: {result['error']}")
#         print(f"Details: {result['details']}")
#         print("\n⚠️ Please run the following commands to train the models:")
#         print("1. cd backend/app/ml/fertilizer_ml")
#         print("2. python train.py")
#         return
    
#     # Print recommendations
#     print("\nTop 3 Recommendations:")
#     for i, rec in enumerate(result["recommendations"], 1):
#         print(f"\n{i}. Crop: {rec['crop']}")
#         print(f"   Confidence: {rec['confidence']:.2%}")
#         if 'soil_compatibility' in rec:
#             print(f"   Soil Compatibility: {rec['soil_compatibility']}%")
#             print(f"   Growth Rate: {rec['growth_rate']}%")
#             print(f"   Yield Potential: {rec['yield_potential']}%")
        
#         print(f"\n   Recommended Fertilizer:")
#         print(f"   - Type: {rec['fertilizer']['type']}")
#         print(f"   - Name: {rec['fertilizer']['name']}")
#         print(f"   - Amount: {rec['fertilizer']['adjusted_amount']} {rec['fertilizer']['unit']}")
#         print("   " + "-" * 40)

# if __name__ == "__main__":
#     # Test the integrated recommendation system
#     test_soil_data = {
#         'N (ppm)': 120,
#         'P (ppm)': 50,
#         'K (ppm)': 130,
#         'Temp (°C)': 28,
#         'Humidity (%)': 55,
#         'pH': 6.2,
#         'Soil Moisture (%)': 145
#     }
    
#     result = get_integrated_recommendation(test_soil_data)
#     print_recommendations(result) 

import os
import sys
from pathlib import Path
from app.ml.crop_ml.prediction_function import predict_crop
from app.ml.fertilizer_ml.test import load_models, predict_fertilizer

# --- Helper functions for calculating success metrics ---

def calculate_soil_compatibility(confidence, ph_value):
    """
    Calculates soil compatibility score.
    - Base score from confidence.
    - Penalizes for pH values far from a general ideal (6.0-7.0).
    """
    base_compatibility = confidence * 100
    ideal_ph_mid = 6.5
    ph_deviation = abs(ph_value - ideal_ph_mid)
    
    ph_penalty = 0
    if ph_deviation > 0.5:  # Penalize if pH is outside 6.0-7.0 range
        ph_penalty = (ph_deviation - 0.5) * 20 # Example: pH 5.0 -> (1.5-0.5)*20 = 20 penalty
    
    compatibility = base_compatibility - ph_penalty
    return round(max(10.0, min(100.0, compatibility)), 2) # Ensure score is between 10 and 100

def calculate_growth_rate(confidence, temp_c, soil_moisture_percent):
    """
    Calculates growth rate score.
    - Base score from confidence.
    - Adjusts based on temperature and soil moisture suitability.
    """
    base_growth = 50 + (confidence * 40)  # Base: 50-90 (higher confidence -> higher base)

    # Temperature factor
    temp_factor = 0
    if 20 <= temp_c <= 30:  # Optimal range
        temp_factor = 10
    elif 15 <= temp_c < 20 or 30 < temp_c <= 35:  # Sub-optimal
        temp_factor = 0
    elif 10 <= temp_c < 15 or 35 < temp_c <= 40:  # Poor
        temp_factor = -10
    else:  # Very poor / Extreme
        temp_factor = -20

    # Soil Moisture factor
    moisture_factor = 0
    if 40 <= soil_moisture_percent <= 70:  # Optimal range
        moisture_factor = 5
    elif 20 <= soil_moisture_percent < 40 or 70 < soil_moisture_percent <= 85:  # Sub-optimal
        moisture_factor = -5
    else:  # Poor (too dry or too wet)
        moisture_factor = -10
        
    growth_rate = base_growth + temp_factor + moisture_factor
    return round(max(30.0, min(100.0, growth_rate)), 2) # Ensure score is between 30 and 100

def calculate_yield_potential(confidence, n_ppm, p_ppm, k_ppm, humidity_percent):
    """
    Calculates yield potential score.
    - Base score from confidence.
    - Adjusts based on general NPK levels and humidity.
    """
    base_yield = 45 + (confidence * 45)  # Base: 45-90

    # NPK factor (simplified general scoring, not crop-specific)
    npk_effect = 0
    # Nitrogen
    if 80 <= n_ppm <= 180: npk_effect += 2
    elif 40 <= n_ppm < 80 or 180 < n_ppm <= 250: npk_effect += 0
    else: npk_effect -= 2 # Too low or too high
    # Phosphorus
    if 40 <= p_ppm <= 80: npk_effect += 2
    elif 20 <= p_ppm < 40 or 80 < p_ppm <= 120: npk_effect += 0
    else: npk_effect -= 2
    # Potassium
    if 80 <= k_ppm <= 180: npk_effect += 2
    elif 40 <= k_ppm < 80 or 180 < k_ppm <= 250: npk_effect += 0
    else: npk_effect -= 2
    
    npk_effect = min(max(npk_effect, -5), 5) # Cap total NPK effect

    # Humidity factor
    humidity_effect = 0
    if 60 <= humidity_percent <= 80:  # Optimal range
        humidity_effect = 5
    elif 40 <= humidity_percent < 60 or 80 < humidity_percent <= 90:  # Sub-optimal
        humidity_effect = -3
    else:  # Poor (too dry or too humid)
        humidity_effect = -8
        
    yield_potential = base_yield + npk_effect + humidity_effect
    return round(max(30.0, min(100.0, yield_potential)), 2) # Ensure score is between 30 and 100

# --- Main integrated recommendation function ---

def check_models_exist():
    """Check if all required model files exist"""
    base_path = Path(__file__).parent / "fertilizer_ml"
    required_files = [
        "fertilizer_type_classifier.pkl",
        "fertilizer_name_classifier.pkl",
        "fertilizer_amount_regressor.pkl",
        "fertilizer_type_encoder.pkl",
        "fertilizer_name_encoder.pkl"
    ]
    
    missing_files = []
    for file in required_files:
        if not (base_path / file).exists():
            missing_files.append(file)
    
    return missing_files

def get_integrated_recommendation(soil_data):
    """
    Get integrated crop and fertilizer recommendations
    
    Args:
        soil_data: dict with keys:
            - 'N (ppm)': Nitrogen content
            - 'P (ppm)': Phosphorus content
            - 'K (ppm)': Potassium content
            - 'Temp (°C)': Temperature
            - 'Humidity (%)': Humidity
            - 'pH': pH level
            - 'Soil Moisture (%)': Soil moisture
    
    Returns:
        dict containing crop recommendations and fertilizer recommendations for each crop
    """
    try:
        missing_files = check_models_exist()
        if missing_files:
            return {
                "error": "Missing model files",
                "details": f"Please train the fertilizer models first. Missing files: {', '.join(missing_files)}",
                "soil_conditions": soil_data
            }
        
        crop_prediction_output = predict_crop(soil_data)

        if isinstance(crop_prediction_output, dict) and "error" in crop_prediction_output:
            return {
                "error": f"Crop prediction failed: {crop_prediction_output.get('error', 'Unknown error')}",
                "details": crop_prediction_output.get('details', ''),
                "soil_conditions": soil_data
            }

        all_probabilities = crop_prediction_output.get('all_crop_probabilities', {})
        
        sorted_crops_by_prob = sorted(all_probabilities.items(), key=lambda item: item[1], reverse=True)
        top_crops_to_consider = [{'crop': crop_name, 'confidence': prob} for crop_name, prob in sorted_crops_by_prob[:3]]

        fertilizer_models = load_models()
        if fertilizer_models is None:
            return {
                "error": "Failed to load fertilizer models",
                "details": "Error loading the trained models. Please ensure models are properly trained.",
                "soil_conditions": soil_data
            }
        
        recommendations_output = {
            "soil_conditions": soil_data,
            "recommendations": []
        }

        for crop_rec in top_crops_to_consider:
            fertilizer_soil_data_for_crop = {
                'N': soil_data['N (ppm)'],
                'P': soil_data['P (ppm)'],
                'K': soil_data['K (ppm)'],
                'pH': soil_data['pH'],
                'OM': 2.0, 
                'Crop Type': crop_rec['crop']
            }
            try:
                fertilizer_rec = predict_fertilizer(fertilizer_soil_data_for_crop, fertilizer_models)

                base_amount = fertilizer_rec['amount']
                confidence = crop_rec['confidence']
                adjusted_amount = base_amount * (0.5 + 0.5 * confidence)

                recommendation = {
                    "crop": crop_rec['crop'],
                    "confidence": crop_rec['confidence'],
                    "fertilizer": {
                        "type": fertilizer_rec['type'],
                        "name": fertilizer_rec['name'],
                        "base_amount": base_amount,
                        "adjusted_amount": round(adjusted_amount, 2),
                        "unit": "kg/m²" if fertilizer_rec['type'] == 'solid' else 'L/m²'
                    }
                }
                
                # Calculate and add more realistic success metrics
                recommendation["soil_compatibility"] = calculate_soil_compatibility(
                    crop_rec['confidence'], 
                    soil_data['pH']
                )
                recommendation["growth_rate"] = calculate_growth_rate(
                    crop_rec['confidence'],
                    soil_data['Temp (°C)'],
                    soil_data['Soil Moisture (%)']
                )
                recommendation["yield_potential"] = calculate_yield_potential(
                    crop_rec['confidence'],
                    soil_data['N (ppm)'],
                    soil_data['P (ppm)'],
                    soil_data['K (ppm)'],
                    soil_data['Humidity (%)']
                )
                
                recommendations_output["recommendations"].append(recommendation)
            except Exception as e:
                print(f"⚠️ Skipping crop '{crop_rec['crop']}' due to error in fertilizer prediction: {e}") 
                continue

        if not recommendations_output["recommendations"]:
            return {
                "error": "No usable crop recommendations",
                "details": "All top crops failed during fertilizer prediction or metric calculation.",
                "soil_conditions": soil_data
            }

        return recommendations_output

    except Exception as e:
        import traceback
        print("Full traceback of the error in get_integrated_recommendation:")
        traceback.print_exc()
        return {
            "error": "Unexpected error in integrated recommendation",
            "details": str(e),
            "soil_conditions": soil_data
        }

def print_recommendations(result):
    """Pretty print the recommendations"""
    print("\n🌱 Integrated Crop and Fertilizer Recommendations")
    print("-" * 60)
    
    if "soil_conditions" in result:
        print("\nSoil Conditions:")
        for key, value in result["soil_conditions"].items():
            print(f"  {key}: {value}")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        if "details" in result:
             print(f"Details: {result['details']}")
        if "Missing model files" in result.get("error", ""):
            print("\n⚠️ Please run the following commands to train the models:")
            print("1. cd backend/app/ml/fertilizer_ml")
            print("2. python train.py")
        return
    
    if "recommendations" in result and result["recommendations"]:
        print("\nTop 3 Recommendations:")
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"\n{i}. Crop: {rec['crop']}")
            print(f"   Confidence: {rec['confidence']:.2%}")
            # These metrics will now be present due to the new calculation logic
            print(f"   Soil Compatibility: {rec.get('soil_compatibility', 'N/A')}%")
            print(f"   Growth Rate: {rec.get('growth_rate', 'N/A')}%")
            print(f"   Yield Potential: {rec.get('yield_potential', 'N/A')}%")
            
            print(f"\n   Recommended Fertilizer:")
            print(f"   - Type: {rec['fertilizer']['type']}")
            print(f"   - Name: {rec['fertilizer']['name']}")
            print(f"   - Amount: {rec['fertilizer']['adjusted_amount']} {rec['fertilizer']['unit']}")
            print("   " + "-" * 40)
    else:
        print("\nNo recommendations available.")

if __name__ == "__main__":
    test_soil_data = {
        'N (ppm)': 120,
        'P (ppm)': 50,
        'K (ppm)': 130,
        'Temp (°C)': 28,
        'Humidity (%)': 55, # Moderate humidity
        'pH': 6.2,
        'Soil Moisture (%)': 60 # Optimal moisture
    }
    
    result = get_integrated_recommendation(test_soil_data)
    print_recommendations(result)

    test_soil_data_2 = {
        'N (ppm)': 10, 
        'P (ppm)': 5, 
        'K (ppm)': 30, 
        'Temp (°C)': 38, # Higher temp
        'Humidity (%)': 95, # Higher humidity
        'pH': 4.5, # Lower pH
        'Soil Moisture (%)': 15 # Lower moisture
    }
    print("\n\n--- Another Test Case (less ideal conditions) ---")
    result_2 = get_integrated_recommendation(test_soil_data_2)
    print_recommendations(result_2)
