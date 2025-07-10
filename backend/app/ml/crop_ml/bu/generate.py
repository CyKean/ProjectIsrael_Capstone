# import pandas as pd
# import numpy as np

# # Define crop data with ranges (mean, standard deviation)
# crop_data = {
#     "Lettuce": [125, 20, 50, 10, 125, 25, 19, 3, 70, 10, 6.5, 0.4, 100, 50, 1, 1, 1005, 10, 55, 15],
#     "Spinach": [175, 25, 60, 12, 150, 30, 20, 4, 70, 10, 6.8, 0.5, 140, 60, 1, 1, 1010, 12, 65, 18],
#     "Pechay": [145, 22, 65, 15, 160, 35, 23, 5, 75, 12, 6.4, 0.3, 180, 70, 2, 1, 1008, 11, 60, 17],
#     "Mustard Greens": [130, 18, 55, 12, 140, 28, 22, 4, 72, 9, 6.6, 0.4, 160, 55, 2, 1, 1006, 10, 58, 16],
#     "Tomatoes": [225, 30, 75, 15, 225, 40, 24, 5, 78, 15, 6.2, 0.5, 200, 80, 2, 1, 1002, 9, 50, 12],
#     "Cucumber": [200, 25, 70, 12, 220, 35, 26, 6, 80, 14, 6.0, 0.5, 190, 75, 2, 1, 1001, 10, 52, 13],
#     "Eggplant": [200, 28, 70, 14, 210, 37, 25, 5, 76, 13, 5.9, 0.5, 195, 78, 2, 1, 1003, 9, 51, 14],
#     "Okra": [180, 24, 65, 13, 205, 33, 27, 5, 79, 13, 6.1, 0.4, 180, 70, 2, 1, 1004, 10, 55, 13],
#     "Carrots": [175, 20, 60, 10, 140, 30, 18, 3, 65, 9, 5.7, 0.3, 130, 50, 2, 1, 1007, 11, 45, 12],
#     "Basil": [125, 18, 55, 10, 135, 28, 20, 4, 66, 9, 6.3, 0.4, 120, 45, 1, 1, 1008, 10, 50, 12],
# }

# # Define column names
# columns = ["N (ppm)", "P (ppm)", "K (ppm)", "Temp (°C)", "Humidity (%)", "pH", 
#            "Rainfall (mm/month)", "Wind Speed (m/s)", "Pressure (hPa)", "Cloud Cover (%)", "Crop"]

# # List to store all data
# all_data = []

# # Number of samples per crop
# num_samples = 200  # Increased for more data points

# # Generate dataset for each crop
# for crop, values in crop_data.items():
#     data = {
#         "N (ppm)": np.random.normal(values[0], values[1], num_samples),
#         "P (ppm)": np.random.normal(values[2], values[3], num_samples),
#         "K (ppm)": np.random.normal(values[4], values[5], num_samples),
#         "Temp (°C)": np.random.normal(values[6], values[7], num_samples),
#         "Humidity (%)": np.random.normal(values[8], values[9], num_samples),
#         "pH": np.random.normal(values[10], values[11], num_samples),
#         "Rainfall (mm/month)": np.random.normal(values[12], values[13], num_samples),
#         "Wind Speed (m/s)": np.random.normal(values[14], values[15], num_samples),
#         "Pressure (hPa)": np.random.normal(values[16], values[17], num_samples),
#         "Cloud Cover (%)": np.random.normal(values[18], values[19], num_samples),
#         "Crop": [crop] * num_samples  # Label each row with the crop name
#     }

#     df = pd.DataFrame(data)

#     # Feature engineering
#     df["NPK Ratio"] = (df["N (ppm)"] + df["P (ppm)"] + df["K (ppm)"]) / 3
#     df["Soil Fertility Index"] = (df["NPK Ratio"] * df["pH"]) / (df["Humidity (%)"] + 1)  # Adding 1 to prevent division by zero
#     df["Adjusted Rainfall"] = df["Rainfall (mm/month)"] + np.random.uniform(-10, 10, num_samples)
    
#     all_data.append(df)

# # Combine all data into a single DataFrame
# final_df = pd.concat(all_data, ignore_index=True)

# # Save dataset as a single CSV file
# output_path = "enhanced_crop_dataset.csv"
# final_df.to_csv(output_path, index=False)

# print(f"Dataset saved successfully: {output_path}")



# import pandas as pd
# import numpy as np

# # Define crop data with ranges (mean, standard deviation)
# crop_data = {
#     "Lettuce": [125, 20, 50, 10, 125, 25, 19, 3, 70, 10, 6.5, 0.4, 100, 50, 1, 1, 1005, 10, 55, 15],
#     "Spinach": [175, 25, 60, 12, 150, 30, 20, 4, 70, 10, 6.8, 0.5, 140, 60, 1, 1, 1010, 12, 65, 18],
#     "Pechay": [145, 22, 65, 15, 160, 35, 23, 5, 75, 12, 6.4, 0.3, 180, 70, 2, 1, 1008, 11, 60, 17],
#     "Mustard Greens": [130, 18, 55, 12, 140, 28, 22, 4, 72, 9, 6.6, 0.4, 160, 55, 2, 1, 1006, 10, 58, 16],
#     "Tomatoes": [225, 30, 75, 15, 225, 40, 24, 5, 78, 15, 6.2, 0.5, 200, 80, 2, 1, 1002, 9, 50, 12],
#     "Cucumber": [200, 25, 70, 12, 220, 35, 26, 6, 80, 14, 6.0, 0.5, 190, 75, 2, 1, 1001, 10, 52, 13],
#     "Eggplant": [200, 28, 70, 14, 210, 37, 25, 5, 76, 13, 5.9, 0.5, 195, 78, 2, 1, 1003, 9, 51, 14],
#     "Okra": [180, 24, 65, 13, 205, 33, 27, 5, 79, 13, 6.1, 0.4, 180, 70, 2, 1, 1004, 10, 55, 13],
#     "Carrots": [175, 20, 60, 10, 140, 30, 18, 3, 65, 9, 5.7, 0.3, 130, 50, 2, 1, 1007, 11, 45, 12],
#     "Basil": [125, 18, 55, 10, 135, 28, 20, 4, 66, 9, 6.3, 0.4, 120, 45, 1, 1, 1008, 10, 50, 12],
# }

# # Define column names
# columns = ["N (ppm)", "P (ppm)", "K (ppm)", "Temp (°C)", "Humidity (%)", "pH", 
#            "Rainfall (mm/month)", "Wind Speed (m/s)", "Pressure (hPa)", "Cloud Cover (%)", "Crop"]

# # List to store all data
# all_data = []

# # Number of samples per crop
# num_samples = 200

# # Generate dataset for each crop
# for crop, values in crop_data.items():
#     data = {col: np.random.normal(values[i * 2], values[i * 2 + 1], num_samples) for i, col in enumerate(columns[:-1])}
    
#     df = pd.DataFrame(data)
#     df["Crop"] = crop  # Label each row with the crop name
    
#     # Feature engineering
#     df["NPK Ratio"] = (df["N (ppm)"] + df["P (ppm)"] + df["K (ppm)"]) / 3
#     df["Soil Fertility Index"] = (df["NPK Ratio"] * df["pH"]) / (df["Humidity (%)"] + 1)
#     df["Soil Moisture (%)"] = np.random.uniform(10, 40, num_samples)  # New feature
    
#     all_data.append(df)

# # Combine all data into a single DataFrame
# final_df = pd.concat(all_data, ignore_index=True)

# # Save dataset as a single CSV file
# output_path = "enhanced_crop_dataset_2.csv"
# final_df.to_csv(output_path, index=False)

# print(f"Dataset saved successfully: {output_path}")


# import pandas as pd
# import numpy as np

# # Define crop data with ranges (values are slightly adjusted for variability)
# crop_data = {
#     "Lettuce": [100, 150, 40, 60, 100, 150, 15, 25, 60, 80, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
#     "Spinach": [150, 200, 50, 70, 120, 180, 15, 25, 60, 80, 6.0, 7.5, 80, 200, 0, 3, 990, 1025, 50, 80],
#     "Pechay": [120, 170, 50, 80, 120, 200, 18, 28, 60, 85, 6.0, 6.8, 100, 250, 0, 2, 990, 1020, 40, 70],
#     "Mustard Greens": [100, 160, 40, 70, 120, 180, 18, 28, 60, 85, 6.0, 7.0, 80, 200, 0, 3, 990, 1020, 50, 75],
#     "Kangkong": [150, 200, 50, 80, 150, 250, 22, 30, 70, 90, 5.5, 7.5, 200, 500, 0, 2, 990, 1020, 50, 90],
#     "Malunggay": [50, 100, 20, 50, 80, 150, 20, 35, 50, 70, 6.0, 7.5, 50, 200, 0, 5, 990, 1025, 40, 70],
#     "Tomatoes": [200, 250, 60, 90, 200, 250, 20, 28, 50, 80, 5.5, 6.5, 100, 300, 0, 3, 990, 1020, 40, 60],
#     "Cucumber": [180, 220, 60, 90, 200, 250, 20, 30, 60, 85, 5.8, 6.5, 100, 300, 0, 3, 990, 1020, 50, 70],
#     "Bell Peppers": [150, 200, 50, 80, 180, 250, 20, 28, 60, 80, 5.5, 6.5, 100, 250, 0, 3, 990, 1020, 40, 60],
#     "Chili Peppers": [120, 180, 50, 80, 150, 200, 20, 30, 50, 80, 5.5, 6.5, 80, 200, 0, 3, 990, 1020, 40, 70],
#     "Eggplant": [180, 220, 50, 80, 180, 250, 22, 30, 60, 85, 5.5, 6.5, 100, 250, 0, 3, 990, 1020, 40, 60],
#     "Ampalaya": [150, 200, 50, 90, 200, 250, 20, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
#     "Okra": [150, 200, 50, 90, 200, 250, 22, 32, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
#     "Patola": [180, 220, 50, 90, 200, 250, 20, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
#     "Upo": [150, 200, 50, 90, 200, 250, 22, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
#     "Kalabasa": [150, 200, 50, 90, 200, 250, 22, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
#     "Sayote": [180, 220, 50, 90, 200, 250, 20, 28, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
#     "Basil": [100, 150, 40, 70, 100, 180, 18, 28, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
#     "Parsley": [100, 150, 40, 70, 100, 180, 18, 28, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
#     "Cilantro": [100, 150, 40, 70, 100, 180, 15, 25, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
#     "Mint": [100, 150, 40, 70, 100, 180, 15, 25, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
#     "Oregano": [100, 150, 40, 70, 100, 180, 18, 28, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
#     "Lemongrass": [150, 200, 50, 90, 150, 250, 22, 30, 50, 75, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
#     "Alugbati": [150, 200, 50, 90, 150, 250, 22, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
#     "Sitaw": [150, 200, 50, 90, 150, 250, 22, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
#     "Kamote Tops": [150, 200, 50, 90, 150, 250, 22, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
#     "Gabi": [180, 220, 50, 90, 150, 250, 20, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
#     "Carrots": [150, 200, 50, 90, 120, 180, 16, 24, 60, 80, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70]
# }

# # Define column names
# columns = [
#     "N (ppm)", "P (ppm)", "K (ppm)", "Temp (°C)", "Humidity (%)", "pH", 
#     "Rainfall (mm/month)", "Wind Speed (m/s)", "Pressure (hPa)", "Cloud Cover (%)", 
#     "NPK Ratio", "Soil Fertility Index", "Soil Moisture (%)", "Crop"
# ]

# # Function to calculate new features
# def calculate_features(N, P, K, pH, Humidity, Rainfall):
#     npk_ratio = (N + P + K) / 3  # Average nutrient value
#     soil_fertility = (N * 0.4 + P * 0.3 + K * 0.3) * (1 if 6.0 <= pH <= 7.0 else 0.8)  # Weighted formula
#     soil_moisture = Humidity * 0.5 + Rainfall * 0.05  # Approximation of moisture retention
#     return npk_ratio, soil_fertility, soil_moisture

# # Generate dataset
# num_samples = 1000  # Adjust as needed
# all_data = []

# for crop, values in crop_data.items():
#     data = {
#         "N (ppm)": np.random.uniform(values[0], values[1], num_samples),
#         "P (ppm)": np.random.uniform(values[2], values[3], num_samples),
#         "K (ppm)": np.random.uniform(values[4], values[5], num_samples),
#         "Temp (°C)": np.random.uniform(values[6], values[7], num_samples),
#         "Humidity (%)": np.random.uniform(values[8], values[9], num_samples),
#         "pH": np.random.uniform(values[10], values[11], num_samples),
#         "Rainfall (mm/month)": np.random.uniform(values[12], values[13], num_samples),
#         "Wind Speed (m/s)": np.random.uniform(values[14], values[15], num_samples),
#         "Pressure (hPa)": np.random.uniform(values[16], values[17], num_samples),
#         "Cloud Cover (%)": np.random.uniform(values[18], values[19], num_samples),
#     }
#     df = pd.DataFrame(data)
    
#     # Calculate new features
#     df["NPK Ratio"], df["Soil Fertility Index"], df["Soil Moisture (%)"] = zip(*df.apply(lambda row: calculate_features(
#         row["N (ppm)"], row["P (ppm)"], row["K (ppm)"], row["pH"], row["Humidity (%)"], row["Rainfall (mm/month)"]), axis=1))
    
#     df["Crop"] = crop  # Assign crop label
#     all_data.append(df)

# # Combine all data
# final_df = pd.concat(all_data, ignore_index=True)

# # Save dataset
# output_path = "crop_dataset.csv"
# final_df.to_csv(output_path, index=False)

# print(f"Enhanced dataset saved successfully: {output_path}")



# import pandas as pd
# import numpy as np

# # Define crop data with improved ranges
# crop_data = {
#     "Lettuce": [100, 150, 40, 60, 100, 150, 15, 25, 60, 80, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
#     "Spinach": [150, 200, 50, 70, 120, 180, 15, 25, 60, 80, 6.0, 7.5, 80, 200, 0, 3, 990, 1025, 50, 80],
#     "Pechay": [120, 170, 50, 80, 120, 200, 18, 28, 60, 85, 6.0, 6.8, 100, 250, 0, 2, 990, 1020, 40, 70],
    # "Mustard Greens": [100, 160, 40, 70, 120, 180, 18, 28, 60, 85, 6.0, 7.0, 80, 200, 0, 3, 990, 1020, 50, 75],
    # "Kangkong": [150, 200, 50, 80, 150, 250, 22, 30, 70, 90, 5.5, 7.5, 200, 500, 0, 2, 990, 1020, 50, 90],
    # "Malunggay": [50, 100, 20, 50, 80, 150, 20, 35, 50, 70, 6.0, 7.5, 50, 200, 0, 5, 990, 1025, 40, 70],
    # "Tomatoes": [200, 250, 60, 90, 200, 250, 20, 28, 50, 80, 5.5, 6.5, 100, 300, 0, 3, 990, 1020, 40, 60],
    # "Cucumber": [180, 220, 60, 90, 200, 250, 20, 30, 60, 85, 5.8, 6.5, 100, 300, 0, 3, 990, 1020, 50, 70],
    # "Bell Peppers": [150, 200, 50, 80, 180, 250, 20, 28, 60, 80, 5.5, 6.5, 100, 250, 0, 3, 990, 1020, 40, 60],
    # "Chili Peppers": [120, 180, 50, 80, 150, 200, 20, 30, 50, 80, 5.5, 6.5, 80, 200, 0, 3, 990, 1020, 40, 70],
    # "Eggplant": [180, 220, 50, 80, 180, 250, 22, 30, 60, 85, 5.5, 6.5, 100, 250, 0, 3, 990, 1020, 40, 60],
    # "Ampalaya": [150, 200, 50, 90, 200, 250, 20, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
    # "Okra": [150, 200, 50, 90, 200, 250, 22, 32, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
    # "Patola": [180, 220, 50, 90, 200, 250, 20, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
    # "Upo": [150, 200, 50, 90, 200, 250, 22, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
    # "Kalabasa": [150, 200, 50, 90, 200, 250, 22, 30, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
    # "Sayote": [180, 220, 50, 90, 200, 250, 20, 28, 60, 85, 5.8, 6.5, 100, 250, 0, 3, 990, 1020, 50, 70],
    # "Basil": [100, 150, 40, 70, 100, 180, 18, 28, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
    # "Parsley": [100, 150, 40, 70, 100, 180, 18, 28, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
    # "Cilantro": [100, 150, 40, 70, 100, 180, 15, 25, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
    # "Mint": [100, 150, 40, 70, 100, 180, 15, 25, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
    # "Oregano": [100, 150, 40, 70, 100, 180, 18, 28, 50, 75, 6.0, 7.0, 50, 150, 0, 2, 990, 1020, 40, 70],
    # "Lemongrass": [150, 200, 50, 90, 150, 250, 22, 30, 50, 75, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
    # "Alugbati": [150, 200, 50, 90, 150, 250, 22, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
    # "Sitaw": [150, 200, 50, 90, 150, 250, 22, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
    # "Kamote Tops": [150, 200, 50, 90, 150, 250, 22, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
    # "Gabi": [180, 220, 50, 90, 150, 250, 20, 30, 60, 85, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70],
    # "Carrots": [150, 200, 50, 90, 120, 180, 16, 24, 60, 80, 5.5, 6.5, 50, 200, 0, 3, 990, 1020, 40, 70]
# }

# columns = [
#     "N (ppm)", "P (ppm)", "K (ppm)", "Temp (°C)", "Humidity (%)", "pH", 
#     "Rainfall (mm/month)", "Wind Speed (m/s)", "Pressure (hPa)", "Cloud Cover (%)", 
#     "NPK Ratio", "Soil Fertility Index", "Soil Moisture (%)", "Crop"
# ]

# # Function to calculate new features
# def calculate_features(N, P, K, pH, Humidity, Rainfall):
#     npk_ratio = (N / (P + 1)) + (K / (P + 1))  # Prevents division by zero
#     fertility_factor = 1 if 6.0 <= pH <= 7.0 else 0.85 if 5.5 <= pH < 6.0 or 7.0 < pH <= 7.5 else 0.7
#     soil_fertility = (N * 0.4 + P * 0.3 + K * 0.3) * fertility_factor
#     soil_moisture = (Humidity * 0.4) + (Rainfall * 0.02)  # Better scaling
#     return npk_ratio, soil_fertility, soil_moisture

# # Generate dataset
# num_samples = 1000
# all_data = []

# for crop, values in crop_data.items():
#     data = {
#         "N (ppm)": np.random.uniform(values[0], values[1], num_samples),
#         "P (ppm)": np.random.uniform(values[2], values[3], num_samples),
#         "K (ppm)": np.random.uniform(values[4], values[5], num_samples),
#         "Temp (°C)": np.random.uniform(values[6], values[7], num_samples),
#         "Humidity (%)": np.random.uniform(values[8], values[9], num_samples),
#         "pH": np.random.uniform(values[10], values[11], num_samples),
#         "Rainfall (mm/month)": np.random.uniform(values[12], values[13], num_samples),
#         "Wind Speed (m/s)": np.random.uniform(values[14], values[15], num_samples),
#         "Pressure (hPa)": np.random.uniform(values[16], values[17], num_samples),
#         "Cloud Cover (%)": np.random.uniform(values[18], values[19], num_samples),
#     }
#     df = pd.DataFrame(data)
    
#     # Calculate new features
#     df["NPK Ratio"], df["Soil Fertility Index"], df["Soil Moisture (%)"] = zip(*df.apply(lambda row: calculate_features(
#         row["N (ppm)"], row["P (ppm)"], row["K (ppm)"], row["pH"], row["Humidity (%)"], row["Rainfall (mm/month)"]), axis=1))
    
#     df["Crop"] = crop
#     all_data.append(df)

# # Combine all data
# final_df = pd.concat(all_data, ignore_index=True)

# # Save dataset
# output_path = "crop_dataset_fixed.csv"
# final_df.to_csv(output_path, index=False)

# print(f"Updated dataset saved successfully: {output_path}")



import pandas as pd
import numpy as np

# Define simplified crop data with relevant ranges
crop_data = {
    "Lettuce": [100, 150, 40, 60, 100, 150, 6.0, 7.0, 60, 80, 50, 150],
    "Spinach": [150, 200, 50, 70, 120, 180, 6.0, 7.5, 60, 80, 80, 200],
    "Pechay": [120, 170, 50, 80, 120, 200, 6.0, 6.8, 60, 85, 100, 250],
    "Mustard Greens": [100, 160, 40, 70, 120, 180, 6.0, 7.0, 60, 85, 80, 200],
    "Tomatoes": [200, 250, 60, 90, 200, 250, 5.5, 6.5, 50, 80, 100, 300],
    "Cucumber": [180, 220, 60, 90, 200, 250, 5.8, 6.5, 60, 85, 100, 300],
    "Bell Peppers": [150, 200, 50, 80, 180, 250, 5.5, 6.5, 60, 80, 100, 250],
    "Chili Peppers": [120, 180, 50, 80, 150, 200, 5.5, 6.5, 50, 80, 80, 200],
    "Eggplant": [180, 220, 50, 80, 180, 250, 5.5, 6.5, 60, 85, 100, 250],
    "Ampalaya": [150, 200, 50, 90, 200, 250, 5.8, 6.5, 60, 85, 100, 250],
    "Okra": [150, 200, 50, 90, 200, 250, 5.8, 6.5, 60, 85, 100, 250],
    "Patola": [180, 220, 50, 90, 200, 250, 5.8, 6.5, 60, 85, 100, 250],
    "Upo": [150, 200, 50, 90, 200, 250, 5.8, 6.5, 60, 85, 100, 250],
    "Kalabasa": [150, 200, 50, 90, 200, 250, 5.8, 6.5, 60, 85, 100, 250],
    "Sayote": [180, 220, 50, 90, 200, 250, 5.8, 6.5, 60, 85, 100, 250],
    "Basil": [100, 150, 40, 70, 100, 180, 6.0, 7.0, 50, 75, 50, 150],
    "Parsley": [100, 150, 40, 70, 100, 180, 6.0, 7.0, 50, 75, 50, 150],
    "Cilantro": [100, 150, 40, 70, 100, 180, 6.0, 7.0, 50, 75, 50, 150],
    "Mint": [100, 150, 40, 70, 100, 180, 6.0, 7.0, 50, 75, 50, 150],
    "Oregano": [100, 150, 40, 70, 100, 180, 6.0, 7.0, 50, 75, 50, 150],
    "Lemongrass": [150, 200, 50, 90, 150, 250, 5.5, 6.5, 50, 75, 50, 200],
    "Alugbati": [150, 200, 50, 90, 150, 250, 5.5, 6.5, 60, 85, 50, 200],
    "Sitaw": [150, 200, 50, 90, 150, 250, 5.5, 6.5, 60, 85, 50, 200],
    "Kamote Tops": [150, 200, 50, 90, 150, 250, 5.5, 6.5, 60, 85, 50, 200],
    "Gabi": [180, 220, 50, 90, 150, 250, 5.5, 6.5, 60, 85, 50, 200],
    "Carrots": [150, 200, 50, 90, 120, 180, 5.5, 6.5, 60, 80, 50, 200],
}


columns = ["N (ppm)", "P (ppm)", "K (ppm)", "Temp (°C)", "Humidity (%)", "pH", "Soil Moisture (%)", "Crop"]

# Function to estimate soil moisture
def estimate_soil_moisture(humidity, rainfall):
    return (humidity * 0.4) + (rainfall * 0.02)

# Generate dataset
num_samples = 1000
all_data = []

for crop, values in crop_data.items():
    nitrogen = np.random.uniform(values[0], values[1], num_samples)
    phosphorus = np.random.uniform(values[2], values[3], num_samples)
    potassium = np.random.uniform(values[4], values[5], num_samples)
    temperature = np.random.uniform(18, 30, num_samples)  # Generic range for simplification
    humidity = np.random.uniform(values[8], values[9], num_samples)
    pH = np.random.uniform(values[6], values[7], num_samples)
    rainfall = np.random.uniform(values[10], values[11], num_samples)
    soil_moisture = estimate_soil_moisture(humidity, rainfall)

    df = pd.DataFrame({
        "N (ppm)": nitrogen,
        "P (ppm)": phosphorus,
        "K (ppm)": potassium,
        "Temp (°C)": temperature,
        "Humidity (%)": humidity,
        "pH": pH,
        "Soil Moisture (%)": soil_moisture,
        "Crop": crop
    })
    all_data.append(df)

# Combine and save dataset
final_df = pd.concat(all_data, ignore_index=True)
output_path = "crop_dataset.csv"
final_df.to_csv(output_path, index=False)

print(f"Dataset saved with limited features: {output_path}")
