# import pandas as pd
# import numpy as np
# import random

# # Define soil nutrient thresholds and fertilizer recommendations
# fertilizer_rules = [
#     # SOLID FERTILIZER:
#     {
#         "name": "FFJ Fermented Plant",
#         "type": "solid",
#         "nutrients": {"N": "high", "K": "medium"},
#         "soil_conditions": {
#             "pH": {"min": 5.5, "max": 7.2}, # Slightly broadened
#             "OM": {"min": 1.0, "max": 3.5}  # Slightly broadened
#         },
#         "amount_range": (2, 4),  # kg per square meter
#         "application_frequency": "monthly"
#     },
#     {
#         "name": "FFJ Fermented Juice Plant",
#         "type": "solid",
#         "nutrients": {"P": "medium", "K": "medium"}, # Relaxed: N requirement removed, K kept at medium
#         "crop_type": ["Fruits"], # Made more specific to Fruits to reduce overlap
#         "soil_conditions": {
#             "pH": {"min": 5.5, "max": 8.0}, # Broadened pH
#             "OM": {"min": 1.0, "max": 4.5}  # Broadened OM
#         },
#         "amount_range": (1, 3),  # kg per square meter
#         "application_frequency": "bi-weekly"
#     },
#     {
#         "name": "Vermi Compost",
#         "type": "solid",
#         "nutrients": {"N": "medium", "P": "medium"}, # Relaxed: K requirement removed
#         "crop_type": ["Corn", "Rice"], # Shifted crop focus
#         "soil_conditions": {
#             "pH": {"min": 5.5, "max": 8.0}, # Broadened pH
#             "OM": {"min": 0.5, "max": 4.0}  # Broadened OM
#         },
#         "amount_range": (3, 5),  # kg per square meter
#         "application_frequency": "quarterly"
#     },
#     # LIQUID FERTILIZER:
#     {
#         "name": "OHN Calpus",
#         "type": "liquid",
#         "nutrients": {"N": "low", "P": "low"}, # Relaxed: K requirement removed
#         "soil_conditions": {
#             "pH": {"min": 5.5, "max": 7.5}, # Broadened
#             "OM": {"min": 0.5, "max": 2.5}  # Added OM condition
#         },
#         "amount_range": (1, 2),  # liters per square meter
#         "application_frequency": "weekly"
#     },
#     {
#         "name": "Wound Vinegar",
#         "type": "liquid",
#         "nutrients": {"K": "low"}, # Made specific to low K
#         "soil_conditions": {
#             "pH": {"min": 5.0, "max": 6.8}, # Slightly more acidic focus
#             "OM": {"min": 1.0, "max": 3.0}  # Added OM condition
#         },
#         "amount_range": (0.5, 1),  # liters per square meter
#         "application_frequency": "bi-weekly"
#     },
#     {
#         "name": "Calcium Phosphate",
#         "type": "liquid",
#         "nutrients": {"P": "high", "Ca": "high"},
#         "soil_conditions": {
#             "pH": {"min": 6.0, "max": 7.8} # Slightly broadened
#         },
#         "amount_range": (1, 2),  # liters per square meter
#         "application_frequency": "monthly"
#     },
#     # Fallback / General Purpose (added to ensure a recommendation is always made)
#     {
#         "name": "Organic Compost",
#         "type": "solid",
#         "nutrients": {"N": "medium", "P": "medium", "K": "medium"}, # General purpose
#         "soil_conditions": { # Broad ranges to act as a fallback
#             "pH": {"min": 4.0, "max": 8.5},
#             "OM": {"min": 0.1, "max": 6.0}
#         },
#         "amount_range": (1.5, 3.5),
#         "application_frequency": "monthly"
#     }
# ]

# # Define thresholds for categorizing nutrient levels
# NUTRIENT_THRESHOLDS = {
#     "N": {"low": 25, "medium": 45},  # N < 25 is low, 25 <= N < 45 is medium, N >= 45 is high
#     "P": {"low": 12, "medium": 22},  # P < 12 is low, 12 <= P < 22 is medium, P >= 22 is high
#     "K": {"low": 55, "medium": 85},  # K < 55 is low, 55 <= K < 85 is medium, K >= 85 is high
# }
# CA_HIGH_THRESHOLD = 1500 # Example threshold for "high" Calcium

# def get_nutrient_category(nutrient_value, nutrient_type):
#     """Categorizes a nutrient value into 'low', 'medium', or 'high'."""
#     if nutrient_type not in NUTRIENT_THRESHOLDS:
#         return "unknown_category" 
    
#     thresholds = NUTRIENT_THRESHOLDS[nutrient_type]
#     if nutrient_value < thresholds["low"]:
#         return "low"
#     elif nutrient_value < thresholds["medium"]:
#         return "medium"
#     else:
#         return "high"

# def recommend_fertilizer(soil_data, crop_type=None):
#     """
#     Recommend fertilizers based on soil conditions and crop type
#     soil_data: dict containing soil parameters (N, P, K, pH, OM, Ca, Crop Type)
#     crop_type: string indicating the recommended crop (passed in soil_data as 'Crop Type')
#     """
#     recommendations = []
    
#     current_om = soil_data.get("OM", 2.0) 
#     current_crop_type = soil_data.get("Crop Type", None) # Get crop_type from soil_data

#     for fertilizer_rule in fertilizer_rules:
#         is_suitable = True

#         # Check crop type condition
#         if "crop_type" in fertilizer_rule:
#             if current_crop_type not in fertilizer_rule["crop_type"]:
#                 is_suitable = False
#                 continue 
        
#         # Check soil pH conditions
#         if "pH" in fertilizer_rule["soil_conditions"]:
#             ph_range = fertilizer_rule["soil_conditions"]["pH"]
#             if not (ph_range["min"] <= soil_data["pH"] <= ph_range["max"]):
#                 is_suitable = False
#                 continue
        
#         # Check organic matter conditions
#         if "OM" in fertilizer_rule["soil_conditions"]:
#             om_range = fertilizer_rule["soil_conditions"]["OM"]
#             if not (om_range["min"] <= current_om <= om_range["max"]):
#                 is_suitable = False
#                 continue

#         # Check nutrient conditions
#         if "nutrients" in fertilizer_rule:
#             for nutrient, required_level in fertilizer_rule["nutrients"].items():
#                 if nutrient in soil_data: 
#                     if nutrient in NUTRIENT_THRESHOLDS:
#                         soil_nutrient_category = get_nutrient_category(soil_data[nutrient], nutrient)
#                         if soil_nutrient_category != required_level.lower(): 
#                             is_suitable = False
#                             break 
#                     elif nutrient == "Ca" and required_level.lower() == "high":
#                         if soil_data.get(nutrient, 0) < CA_HIGH_THRESHOLD: 
#                             is_suitable = False
#                             break
#                 elif required_level.lower() != "any": 
#                     is_suitable = False
#                     break
#             if not is_suitable: 
#                 continue
        
#         if is_suitable:
#             amount = np.random.uniform(*fertilizer_rule["amount_range"])
#             recommendations.append({
#                 "type": fertilizer_rule["type"],
#                 "name": fertilizer_rule["name"],
#                 "amount": round(amount, 2),
#                 "unit": "kg/m²" if fertilizer_rule["type"] == "solid" else "L/m²",
#                 "frequency": fertilizer_rule["application_frequency"]
#             })
    
#     if not recommendations and fertilizer_rules:
#          fallback_rule = fertilizer_rules[-1] 
#          if fallback_rule['name'] == "Organic Compost": 
#             amount = np.random.uniform(*fallback_rule["amount_range"])
#             recommendations.append({
#                 "type": fallback_rule["type"],
#                 "name": fallback_rule["name"],
#                 "amount": round(amount, 2),
#                 "unit": "kg/m²" if fallback_rule["type"] == "solid" else "L/m²",
#                 "frequency": fallback_rule["application_frequency"]
#             })

#     if not recommendations:
#         return [{
#             "type": "solid",
#             "name": "General Purpose Compost", # A very generic fallback
#             "amount": 1.0, 
#             "unit": "kg/m²",
#             "frequency": "as needed"
#         }]
            
#     return recommendations

# # Generate synthetic soil data
# num_samples = 5000
# data = []

# for _ in range(num_samples):
#     soil_data_for_generation = { # Renamed to avoid confusion
#         "N": np.random.uniform(5, 60),    
#         "P": np.random.uniform(5, 40),    
#         "K": np.random.uniform(20, 120),  
#         "pH": np.random.uniform(4.5, 8.0),  
#         "OM": np.random.uniform(0.5, 5.0), 
#         "Ca": np.random.uniform(500, 2500),
#         "Crop Type": np.random.choice(["Rice", "Corn", "Vegetables", "Fruits"]) # Include Crop Type here
#     }
    
#     all_recommendations = recommend_fertilizer(soil_data_for_generation) # Pass the full soil_data
    
#     recommendations_to_store = [random.choice(all_recommendations)] if all_recommendations else []
    
#     data.append({
#         "Nitrogen (mg/kg)": soil_data_for_generation["N"],
#         "Phosphorus (mg/kg)": soil_data_for_generation["P"],
#         "Potassium (mg/kg)": soil_data_for_generation["K"],
#         "pH": soil_data_for_generation["pH"],
#         "Organic Matter (%)": soil_data_for_generation["OM"],
#         # "Calcium (mg/kg)": soil_data_for_generation["Ca"], # Keep commented if not a direct feature for ML
#         "Crop Type": soil_data_for_generation["Crop Type"],
#         "Fertilizer Recommendations": recommendations_to_store 
#     })

# df = pd.DataFrame(data)

# df.to_csv("soil_fertilizer_dataset.csv", index=False)
# print("✅ Synthetic dataset generated: 'soil_fertilizer_dataset.csv'!")
import pandas as pd
import numpy as np
import random

# Define soil nutrient thresholds and fertilizer recommendations
fertilizer_rules = [
    # SOLID FERTILIZER:
    {
        "name": "FFJ Fermented Plant", # Keep as is, count is decent
        "type": "solid",
        "nutrients": {"N": "high", "K": "medium"},
        "soil_conditions": {
            "pH": {"min": 5.5, "max": 7.2},
            "OM": {"min": 1.0, "max": 3.5}
        },
        "amount_range": (2, 4),
        "application_frequency": "monthly"
    },
    {
        "name": "FFJ Fermented Juice Plant", # Target for improvement
        "type": "solid",
        "nutrients": {"P": "high", "K": "high"}, # Made more specific: High P and High K
        "crop_type": ["Fruits"], # Kept specific to Fruits
        "soil_conditions": {
            "pH": {"min": 6.0, "max": 7.5}, # Slightly less broad than before
            "OM": {"min": 2.0, "max": 4.0}  # Targeting higher OM
        },
        "amount_range": (1, 3),
        "application_frequency": "bi-weekly"
    },
    {
        "name": "Vermi Compost", # Count is good, maintain
        "type": "solid",
        "nutrients": {"N": "medium", "P": "medium"},
        "crop_type": ["Corn", "Rice", "Vegetables"], # Broadened crop type slightly
        "soil_conditions": {
            "pH": {"min": 5.5, "max": 8.0},
            "OM": {"min": 0.5, "max": 4.0}
        },
        "amount_range": (3, 5),
        "application_frequency": "quarterly"
    },
    # LIQUID FERTILIZER:
    {
        "name": "OHN Calpus", # Target for improvement
        "type": "liquid",
        "nutrients": {"N": "low", "P": "low", "K": "low"}, # Specific: all low
        "crop_type": ["Vegetables"], # Made specific to Vegetables
        "soil_conditions": {
            "pH": {"min": 6.0, "max": 7.0}, # More specific pH
            "OM": {"min": 0.5, "max": 2.0}  # More specific OM
        },
        "amount_range": (1, 2),
        "application_frequency": "weekly"
    },
    {
        "name": "Wound Vinegar", # Count is good, maintain
        "type": "liquid",
        "nutrients": {"K": "low"},
        "crop_type": ["Fruits", "Corn"], # Added Corn as an option
        "soil_conditions": {
            "pH": {"min": 5.0, "max": 6.8},
            "OM": {"min": 1.0, "max": 3.0}
        },
        "amount_range": (0.5, 1),
        "application_frequency": "bi-weekly"
    },
    {
        "name": "Calcium Phosphate", # Count is good, maintain
        "type": "liquid",
        "nutrients": {"P": "high", "Ca": "high"},
        "soil_conditions": {
            "pH": {"min": 6.0, "max": 7.8}
        },
        "amount_range": (1, 2),
        "application_frequency": "monthly"
    },
    {
        "name": "Organic Compost", # Fallback
        "type": "solid",
        "nutrients": {"N": "medium", "P": "medium", "K": "medium"},
        "soil_conditions": {
            "pH": {"min": 4.0, "max": 8.5},
            "OM": {"min": 0.1, "max": 6.0}
        },
        "amount_range": (1.5, 3.5),
        "application_frequency": "monthly"
    }
]

# Define thresholds for categorizing nutrient levels
NUTRIENT_THRESHOLDS = {
    "N": {"low": 25, "medium": 45},
    "P": {"low": 12, "medium": 22}, # P < 12 is low, 12-22 is medium, >22 is high
    "K": {"low": 55, "medium": 85}, # K < 55 is low, 55-85 is medium, >85 is high
}
CA_HIGH_THRESHOLD = 1500

def get_nutrient_category(nutrient_value, nutrient_type):
    if nutrient_type not in NUTRIENT_THRESHOLDS:
        return "unknown_category"
    
    thresholds = NUTRIENT_THRESHOLDS[nutrient_type]
    if nutrient_value < thresholds["low"]:
        return "low"
    elif nutrient_value < thresholds["medium"]: # Corrected: was nutrient_value < thresholds["high"]
        return "medium"
    else:
        return "high"

def recommend_fertilizer(soil_data): # Removed crop_type as direct arg, get from soil_data
    recommendations = []
    
    current_om = soil_data.get("OM", 2.0) 
    current_crop_type = soil_data.get("Crop Type", None)

    for fertilizer_rule in fertilizer_rules:
        is_suitable = True

        if "crop_type" in fertilizer_rule:
            if current_crop_type not in fertilizer_rule["crop_type"]:
                is_suitable = False
                continue 
        
        if "pH" in fertilizer_rule["soil_conditions"]:
            ph_range = fertilizer_rule["soil_conditions"]["pH"]
            if not (ph_range["min"] <= soil_data["pH"] <= ph_range["max"]):
                is_suitable = False
                continue
        
        if "OM" in fertilizer_rule["soil_conditions"]:
            om_range = fertilizer_rule["soil_conditions"]["OM"]
            if not (om_range["min"] <= current_om <= om_range["max"]):
                is_suitable = False
                continue

        if "nutrients" in fertilizer_rule:
            for nutrient, required_level in fertilizer_rule["nutrients"].items():
                if nutrient in soil_data: 
                    if nutrient in NUTRIENT_THRESHOLDS:
                        soil_nutrient_category = get_nutrient_category(soil_data[nutrient], nutrient)
                        if soil_nutrient_category != required_level.lower(): 
                            is_suitable = False
                            break 
                    elif nutrient == "Ca" and required_level.lower() == "high":
                        if soil_data.get(nutrient, 0) < CA_HIGH_THRESHOLD: 
                            is_suitable = False
                            break
                elif required_level.lower() != "any": 
                    is_suitable = False
                    break
            if not is_suitable: 
                continue
        
        if is_suitable:
            amount = np.random.uniform(*fertilizer_rule["amount_range"])
            recommendations.append({
                "type": fertilizer_rule["type"],
                "name": fertilizer_rule["name"],
                "amount": round(amount, 2),
                "unit": "kg/m²" if fertilizer_rule["type"] == "solid" else "L/m²",
                "frequency": fertilizer_rule["application_frequency"]
            })
    
    if not recommendations and fertilizer_rules:
         fallback_rule = fertilizer_rules[-1] 
         if fallback_rule['name'] == "Organic Compost": 
            amount = np.random.uniform(*fallback_rule["amount_range"])
            recommendations.append({
                "type": fallback_rule["type"],
                "name": fallback_rule["name"],
                "amount": round(amount, 2),
                "unit": "kg/m²" if fallback_rule["type"] == "solid" else "L/m²",
                "frequency": fallback_rule["application_frequency"]
            })

    if not recommendations:
        return [{
            "type": "solid",
            "name": "General Purpose Compost",
            "amount": 1.0, 
            "unit": "kg/m²",
            "frequency": "as needed"
        }]
            
    return recommendations

# Generate synthetic soil data
num_samples = 5000
data = []

for _ in range(num_samples):
    soil_data_for_generation = {
        "N": np.random.uniform(5, 60),    
        "P": np.random.uniform(5, 40),    
        "K": np.random.uniform(20, 120),  
        "pH": np.random.uniform(4.5, 8.0),  
        "OM": np.random.uniform(0.5, 5.0), 
        "Ca": np.random.uniform(500, 2500),
        "Crop Type": np.random.choice(["Rice", "Corn", "Vegetables", "Fruits"])
    }
    
    all_recommendations = recommend_fertilizer(soil_data_for_generation)
    
    recommendations_to_store = [random.choice(all_recommendations)] if all_recommendations else []
    
    data.append({
        "Nitrogen (mg/kg)": soil_data_for_generation["N"],
        "Phosphorus (mg/kg)": soil_data_for_generation["P"],
        "Potassium (mg/kg)": soil_data_for_generation["K"],
        "pH": soil_data_for_generation["pH"],
        "Organic Matter (%)": soil_data_for_generation["OM"],
        "Crop Type": soil_data_for_generation["Crop Type"],
        "Fertilizer Recommendations": recommendations_to_store 
    })

df = pd.DataFrame(data)

df.to_csv("soil_fertilizer_dataset.csv", index=False)
print("✅ Synthetic dataset generated: 'soil_fertilizer_dataset.csv'!")
