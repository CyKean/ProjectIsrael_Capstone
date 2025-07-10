import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
import warnings
import ast
warnings.filterwarnings('ignore')

# Load dataset
print("Loading dataset...")
df = pd.read_csv("soil_fertilizer_dataset.csv")

# Function to safely extract fertilizer information
def extract_fertilizer_info(recommendation):
    try:
        if isinstance(recommendation, str):
            # Convert string representation of list to actual list
            recommendations = ast.literal_eval(recommendation)
        else:
            recommendations = recommendation
            
        if recommendations and len(recommendations) > 0:
            # Get the first recommendation
            rec = recommendations[0]
            return {
                'type': rec.get('type', 'unknown'),      # 'type' key is correct from generate.py
                'fertilizer': rec.get('name', 'unknown'), # Key in generate.py is 'name' for fertilizer name
                'amount': float(rec.get('amount', 0))
            }
        return {'type': 'unknown', 'fertilizer': 'unknown', 'amount': 0.0}
    except Exception as e:
        print(f"Error extracting fertilizer info for recommendation '{recommendation}': {e}") # More informative error
        return {'type': 'unknown', 'fertilizer': 'unknown', 'amount': 0.0}

# Extract fertilizer information
print("\nExtracting fertilizer information...")
fertilizer_info = df['Fertilizer Recommendations'].apply(extract_fertilizer_info)
df['Fertilizer Type'] = fertilizer_info.apply(lambda x: x['type'])
df['Fertilizer Name'] = fertilizer_info.apply(lambda x: x['fertilizer'])
df['Amount'] = fertilizer_info.apply(lambda x: x['amount'])

# Print unique values and their counts
print("\nUnique Fertilizer Types and counts:")
print(df['Fertilizer Type'].value_counts())

print("\nUnique Fertilizer Names and counts:")
print(df['Fertilizer Name'].value_counts())

print("\nSample Amounts:")
print(df['Amount'].describe())

# Remove rows with unknown values
print("\nRemoving rows with unknown values...")
df = df[df['Fertilizer Type'] != 'unknown']
df = df[df['Fertilizer Name'] != 'unknown']

# Prepare features and targets
X = df[["Nitrogen (mg/kg)", "Phosphorus (mg/kg)", "Potassium (mg/kg)", "pH", "Organic Matter (%)", "Crop Type"]]


# Encode fertilizer type and name
print("\nEncoding fertilizer types and names...")
type_encoder = LabelEncoder()
name_encoder = LabelEncoder()

# Fit and transform the encoders
y_type = type_encoder.fit_transform(df['Fertilizer Type'])
y_name = name_encoder.fit_transform(df['Fertilizer Name'])
y_amount = df['Amount']

# Print encoded values
print("\nFertilizer Type encoding mapping:")
for i, label in enumerate(type_encoder.classes_):
    print(f"{label} -> {i}")

print("\nFertilizer Name encoding mapping:")
for i, label in enumerate(name_encoder.classes_):
    print(f"{label} -> {i}")

# Create preprocessing pipeline
numeric_features = ["Nitrogen (mg/kg)", "Phosphorus (mg/kg)", "Potassium (mg/kg)", "pH", "Organic Matter (%)"]
categorical_features = ["Crop Type"]
preprocessor = ColumnTransformer(
    transformers=[
        ('num', RobustScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Split data
X_train, X_test, y_type_train, y_type_test = train_test_split(
    X, y_type, test_size=0.2, random_state=42, stratify=y_type
)
_, _, y_name_train, y_name_test = train_test_split(
    X, y_name, test_size=0.2, random_state=42, stratify=y_name
)
_, _, y_amount_train, y_amount_test = train_test_split(
    X, y_amount, test_size=0.2, random_state=42
)

# Train Fertilizer Type Classifier
print("\nTraining Fertilizer Type Classifier...")
type_pipeline = ImbPipeline([
    ('preprocessor_type', preprocessor), # Renamed to avoid conflict if preprocessor is tuned separately
    ('sampler_type', SMOTE(random_state=42, k_neighbors=1)),
    ('classifier_type', RandomForestClassifier(n_estimators=200, random_state=42))
])

type_pipeline.fit(X_train, y_type_train)
type_preds = type_pipeline.predict(X_test)
type_accuracy = accuracy_score(y_type_test, type_preds)
print(f"Fertilizer Type Classification Accuracy: {type_accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_type_test, type_preds))

# Train Fertilizer Name Classifier
print("\nTraining Fertilizer Name Classifier...")
name_pipeline_base = ImbPipeline([
    ('preprocessor', preprocessor),
    # ('under_sampler', RandomUnderSampler(sampling_strategy='auto', random_state=42)), # Consider uncommenting this if Organic Compost is still too dominant
    ('sampler', SMOTE(random_state=42, k_neighbors=1)),
    ('classifier', GradientBoostingClassifier(random_state=42)) # n_estimators will be tuned
])

param_grid_name = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__learning_rate': [0.01, 0.05, 0.1],
    'classifier__max_depth': [3, 4, 5]
}
grid_search_name = GridSearchCV(name_pipeline_base, param_grid_name, cv=3, scoring='accuracy', n_jobs=-1, verbose=1)
grid_search_name.fit(X_train, y_name_train)
print(f"Best parameters for Fertilizer Name: {grid_search_name.best_params_}")
name_pipeline = grid_search_name.best_estimator_ # Use the best found pipeline

name_preds = name_pipeline.predict(X_test)
name_accuracy = accuracy_score(y_name_test, name_preds)
print(f"Fertilizer Name Classification Accuracy: {name_accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_name_test, name_preds))

# Train Amount Regressor
print("\nTraining Amount Regressor...")
amount_pipeline_base = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', GradientBoostingRegressor(random_state=42))
])

param_grid_amount = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__learning_rate': [0.01, 0.05, 0.1],
    'regressor__max_depth': [3, 4, 5],
    'regressor__loss': ['squared_error', 'absolute_error', 'huber']
}
grid_search_amount = GridSearchCV(amount_pipeline_base, param_grid_amount, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=1)
grid_search_amount.fit(X_train, y_amount_train)
print(f"Best parameters for Amount Regressor: {grid_search_amount.best_params_}")
amount_pipeline = grid_search_amount.best_estimator_

amount_preds = amount_pipeline.predict(X_test)
amount_mae = mean_absolute_error(y_amount_test, amount_preds)

print(f"Amount Prediction MAE: {amount_mae:.4f}")

# Save models and encoders
print("\nSaving models and encoders...")
joblib.dump(type_pipeline, "fertilizer_type_classifier.pkl")
joblib.dump(name_pipeline, "fertilizer_name_classifier.pkl")
joblib.dump(amount_pipeline, "fertilizer_amount_regressor.pkl")
joblib.dump(type_encoder, "fertilizer_type_encoder.pkl")
joblib.dump(name_encoder, "fertilizer_name_encoder.pkl")

print("\n✅ All models trained and saved successfully!")

# Test the saved models
print("\nTesting saved models...")
test_data = {
    'N (ppm)': 120,
    'P (ppm)': 50,
    'K (ppm)': 130,
    'pH': 6.2,
    'OM': 2.0,
    'Crop Type': 'Rice' # Added Crop Type for testing
}

X_test_sample = pd.DataFrame({
    "Nitrogen (mg/kg)": [test_data['N (ppm)']],
    "Phosphorus (mg/kg)": [test_data['P (ppm)']],
    "Potassium (mg/kg)": [test_data['K (ppm)']],
    "pH": [test_data['pH']],
    "Organic Matter (%)": [test_data['OM']],
    "Crop Type": [test_data['Crop Type']] # Added Crop Type
})

type_pred = type_pipeline.predict(X_test_sample)
name_pred = name_pipeline.predict(X_test_sample)
amount_pred = amount_pipeline.predict(X_test_sample)

print("\nTest Prediction:")
print(f"Fertilizer Type: {type_encoder.inverse_transform(type_pred)[0]}")
print(f"Fertilizer Name: {name_encoder.inverse_transform(name_pred)[0]}")
print(f"Amount: {amount_pred[0]:.2f}")
