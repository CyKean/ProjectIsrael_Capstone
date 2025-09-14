import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, PowerTransformer, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import os
import joblib
import seaborn as sns
from datetime import datetime

# 20 Different Parameter Sets (from lowest to highest expected accuracy)
configurations = [
    # 1. Very Simple Model (Lowest Expected Accuracy)
    {
        "name": "Very_Simple_Model",
        "MIN_SAMPLES_PER_CLASS": 10,
        "K_FEATURES": 15,
        "TEST_SIZE": 0.3,
        "VAL_SIZE": 0.2,
        "NN_EPOCHS": 50,
        "NN_BATCH_SIZE": 64,
        "NN_LEARNING_RATE": 0.01,
        "NN_L2_REG": 0.0001,
        "NN_DROPOUT_RATES": [0.1, 0.1],
        "NN_LAYERS": [64],
        "XGB_LEARNING_RATE": 0.3,
        "XGB_ESTIMATORS": 50,
        "XGB_MAX_DEPTH": 3,
        "XGB_SUBSAMPLE": 0.6,
        "XGB_COLSAMPLE_BYTREE": 0.6,
        "XGB_GAMMA": 0,
        "PREPROCESSING_METHOD": "standard",
        "FEATURE_SELECTION_METHOD": "f_classif",
        "SAMPLING_METHOD": "none",
        "ACTIVATION": "relu"
    },
    
    # 2. Simple Model with Basic Regularization
    {
        "name": "Simple_Regularized",
        "MIN_SAMPLES_PER_CLASS": 8,
        "K_FEATURES": 20,
        "TEST_SIZE": 0.25,
        "VAL_SIZE": 0.2,
        "NN_EPOCHS": 80,
        "NN_BATCH_SIZE": 48,
        "NN_LEARNING_RATE": 0.005,
        "NN_L2_REG": 0.001,
        "NN_DROPOUT_RATES": [0.2, 0.1],
        "NN_LAYERS": [64, 32],
        "XGB_LEARNING_RATE": 0.2,
        "XGB_ESTIMATORS": 75,
        "XGB_MAX_DEPTH": 4,
        "XGB_SUBSAMPLE": 0.7,
        "XGB_COLSAMPLE_BYTREE": 0.7,
        "XGB_GAMMA": 0.1,
        "PREPROCESSING_METHOD": "standard",
        "FEATURE_SELECTION_METHOD": "f_classif",
        "SAMPLING_METHOD": "none",
        "ACTIVATION": "relu"
    },
    
    # 3. Basic Model with SMOTE
    {
        "name": "Basic_with_SMOTE",
        "MIN_SAMPLES_PER_CLASS": 6,
        "K_FEATURES": 25,
        "TEST_SIZE": 0.2,
        "VAL_SIZE": 0.2,
        "NN_EPOCHS": 100,
        "NN_BATCH_SIZE": 32,
        "NN_LEARNING_RATE": 0.002,
        "NN_L2_REG": 0.002,
        "NN_DROPOUT_RATES": [0.3, 0.2],
        "NN_LAYERS": [128, 64],
        "XGB_LEARNING_RATE": 0.1,
        "XGB_ESTIMATORS": 100,
        "XGB_MAX_DEPTH": 5,
        "XGB_SUBSAMPLE": 0.8,
        "XGB_COLSAMPLE_BYTREE": 0.8,
        "XGB_GAMMA": 0.1,
        "PREPROCESSING_METHOD": "standard",
        "FEATURE_SELECTION_METHOD": "f_classif",
        "SAMPLING_METHOD": "smote",
        "ACTIVATION": "relu"
    },
    
    # 4. Standard Model
    {
        "name": "Standard_Model",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 30,
        "TEST_SIZE": 0.2,
        "VAL_SIZE": 0.2,
        "NN_EPOCHS": 120,
        "NN_BATCH_SIZE": 32,
        "NN_LEARNING_RATE": 0.001,
        "NN_L2_REG": 0.002,
        "NN_DROPOUT_RATES": [0.3, 0.2, 0.1],
        "NN_LAYERS": [128, 64, 32],
        "XGB_LEARNING_RATE": 0.1,
        "XGB_ESTIMATORS": 100,
        "XGB_MAX_DEPTH": 6,
        "XGB_SUBSAMPLE": 0.8,
        "XGB_COLSAMPLE_BYTREE": 0.8,
        "XGB_GAMMA": 0.1,
        "PREPROCESSING_METHOD": "standard",
        "FEATURE_SELECTION_METHOD": "f_classif",
        "SAMPLING_METHOD": "smote",
        "ACTIVATION": "relu"
    },
    
    # 5. Standard with Power Transform
    {
        "name": "Standard_PowerTransform",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 30,
        "TEST_SIZE": 0.2,
        "VAL_SIZE": 0.2,
        "NN_EPOCHS": 120,
        "NN_BATCH_SIZE": 32,
        "NN_LEARNING_RATE": 0.001,
        "NN_L2_REG": 0.002,
        "NN_DROPOUT_RATES": [0.3, 0.2, 0.1],
        "NN_LAYERS": [128, 64, 32],
        "XGB_LEARNING_RATE": 0.1,
        "XGB_ESTIMATORS": 100,
        "XGB_MAX_DEPTH": 6,
        "XGB_SUBSAMPLE": 0.8,
        "XGB_COLSAMPLE_BYTREE": 0.8,
        "XGB_GAMMA": 0.1,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "f_classif",
        "SAMPLING_METHOD": "smote",
        "ACTIVATION": "relu"
    },
    
    # 6. Standard with Mutual Info
    {
        "name": "Standard_MutualInfo",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 30,
        "TEST_SIZE": 0.2,
        "VAL_SIZE": 0.2,
        "NN_EPOCHS": 120,
        "NN_BATCH_SIZE": 32,
        "NN_LEARNING_RATE": 0.001,
        "NN_L2_REG": 0.002,
        "NN_DROPOUT_RATES": [0.3, 0.2, 0.1],
        "NN_LAYERS": [128, 64, 32],
        "XGB_LEARNING_RATE": 0.1,
        "XGB_ESTIMATORS": 100,
        "XGB_MAX_DEPTH": 6,
        "XGB_SUBSAMPLE": 0.8,
        "XGB_COLSAMPLE_BYTREE": 0.8,
        "XGB_GAMMA": 0.1,
        "PREPROCESSING_METHOD": "standard",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "smote",
        "ACTIVATION": "relu"
    },
    
    # 7. Standard with ADASYN
    {
        "name": "Standard_ADASYN",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 30,
        "TEST_SIZE": 0.2,
        "VAL_SIZE": 0.2,
        "NN_EPOCHS": 120,
        "NN_BATCH_SIZE": 32,
        "NN_LEARNING_RATE": 0.001,
        "NN_L2_REG": 0.002,
        "NN_DROPOUT_RATES": [0.3, 0.2, 0.1],
        "NN_LAYERS": [128, 64, 32],
        "XGB_LEARNING_RATE": 0.1,
        "XGB_ESTIMATORS": 100,
        "XGB_MAX_DEPTH": 6,
        "XGB_SUBSAMPLE": 0.8,
        "XGB_COLSAMPLE_BYTREE": 0.8,
        "XGB_GAMMA": 0.1,
        "PREPROCESSING_METHOD": "standard",
        "FEATURE_SELECTION_METHOD": "f_classif",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "relu"
    },
    
    # 8. Enhanced Model
    {
        "name": "Enhanced_Model",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 35,
        "TEST_SIZE": 0.2,
        "VAL_SIZE": 0.15,
        "NN_EPOCHS": 150,
        "NN_BATCH_SIZE": 32,
        "NN_LEARNING_RATE": 0.0008,
        "NN_L2_REG": 0.003,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2],
        "NN_LAYERS": [256, 128, 64],
        "XGB_LEARNING_RATE": 0.08,
        "XGB_ESTIMATORS": 120,
        "XGB_MAX_DEPTH": 7,
        "XGB_SUBSAMPLE": 0.85,
        "XGB_COLSAMPLE_BYTREE": 0.85,
        "XGB_GAMMA": 0.2,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 9. Enhanced with Robust Scaling
    {
        "name": "Enhanced_Robust",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 35,
        "TEST_SIZE": 0.2,
        "VAL_SIZE": 0.15,
        "NN_EPOCHS": 150,
        "NN_BATCH_SIZE": 32,
        "NN_LEARNING_RATE": 0.0008,
        "NN_L2_REG": 0.003,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2],
        "NN_LAYERS": [256, 128, 64],
        "XGB_LEARNING_RATE": 0.08,
        "XGB_ESTIMATORS": 120,
        "XGB_MAX_DEPTH": 7,
        "XGB_SUBSAMPLE": 0.85,
        "XGB_COLSAMPLE_BYTREE": 0.85,
        "XGB_GAMMA": 0.2,
        "PREPROCESSING_METHOD": "robust",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 10. High Capacity Model
    {
        "name": "High_Capacity",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 40,
        "TEST_SIZE": 0.15,
        "VAL_SIZE": 0.15,
        "NN_EPOCHS": 200,
        "NN_BATCH_SIZE": 24,
        "NN_LEARNING_RATE": 0.0005,
        "NN_L2_REG": 0.005,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2, 0.1],
        "NN_LAYERS": [256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.05,
        "XGB_ESTIMATORS": 150,
        "XGB_MAX_DEPTH": 8,
        "XGB_SUBSAMPLE": 0.9,
        "XGB_COLSAMPLE_BYTREE": 0.9,
        "XGB_GAMMA": 0.3,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 11. High Capacity with More Features
    {
        "name": "High_Capacity_More_Features",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 45,
        "TEST_SIZE": 0.15,
        "VAL_SIZE": 0.15,
        "NN_EPOCHS": 200,
        "NN_BATCH_SIZE": 24,
        "NN_LEARNING_RATE": 0.0005,
        "NN_L2_REG": 0.005,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2, 0.1],
        "NN_LAYERS": [256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.05,
        "XGB_ESTIMATORS": 150,
        "XGB_MAX_DEPTH": 8,
        "XGB_SUBSAMPLE": 0.9,
        "XGB_COLSAMPLE_BYTREE": 0.9,
        "XGB_GAMMA": 0.3,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 12. High Capacity with Less Regularization
    {
        "name": "High_Capacity_Less_Reg",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 45,
        "TEST_SIZE": 0.15,
        "VAL_SIZE": 0.15,
        "NN_EPOCHS": 200,
        "NN_BATCH_SIZE": 24,
        "NN_LEARNING_RATE": 0.0005,
        "NN_L2_REG": 0.001,
        "NN_DROPOUT_RATES": [0.3, 0.2, 0.1, 0.1],
        "NN_LAYERS": [256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.05,
        "XGB_ESTIMATORS": 150,
        "XGB_MAX_DEPTH": 8,
        "XGB_SUBSAMPLE": 0.9,
        "XGB_COLSAMPLE_BYTREE": 0.9,
        "XGB_GAMMA": 0.1,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 13. High Capacity with More Regularization
    {
        "name": "High_Capacity_More_Reg",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 45,
        "TEST_SIZE": 0.15,
        "VAL_SIZE": 0.15,
        "NN_EPOCHS": 200,
        "NN_BATCH_SIZE": 24,
        "NN_LEARNING_RATE": 0.0005,
        "NN_L2_REG": 0.01,
        "NN_DROPOUT_RATES": [0.5, 0.4, 0.3, 0.2],
        "NN_LAYERS": [256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.05,
        "XGB_ESTIMATORS": 150,
        "XGB_MAX_DEPTH": 8,
        "XGB_SUBSAMPLE": 0.8,
        "XGB_COLSAMPLE_BYTREE": 0.8,
        "XGB_GAMMA": 0.5,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 14. Very High Capacity Model
    {
        "name": "Very_High_Capacity",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 50,
        "TEST_SIZE": 0.1,
        "VAL_SIZE": 0.1,
        "NN_EPOCHS": 250,
        "NN_BATCH_SIZE": 16,
        "NN_LEARNING_RATE": 0.0003,
        "NN_L2_REG": 0.005,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2, 0.1, 0.1],
        "NN_LAYERS": [512, 256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.03,
        "XGB_ESTIMATORS": 200,
        "XGB_MAX_DEPTH": 9,
        "XGB_SUBSAMPLE": 0.9,
        "XGB_COLSAMPLE_BYTREE": 0.9,
        "XGB_GAMMA": 0.4,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 15. Very High Capacity with UnderSampling
    {
        "name": "Very_High_Capacity_UnderSample",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 50,
        "TEST_SIZE": 0.1,
        "VAL_SIZE": 0.1,
        "NN_EPOCHS": 250,
        "NN_BATCH_SIZE": 16,
        "NN_LEARNING_RATE": 0.0003,
        "NN_L2_REG": 0.005,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2, 0.1, 0.1],
        "NN_LAYERS": [512, 256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.03,
        "XGB_ESTIMATORS": 200,
        "XGB_MAX_DEPTH": 9,
        "XGB_SUBSAMPLE": 0.9,
        "XGB_COLSAMPLE_BYTREE": 0.9,
        "XGB_GAMMA": 0.4,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "undersample",
        "ACTIVATION": "leaky_relu"
    },
    
    # 16. Very High Capacity with No Sampling
    {
        "name": "Very_High_Capacity_No_Sampling",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 50,
        "TEST_SIZE": 0.1,
        "VAL_SIZE": 0.1,
        "NN_EPOCHS": 250,
        "NN_BATCH_SIZE": 16,
        "NN_LEARNING_RATE": 0.0003,
        "NN_L2_REG": 0.005,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2, 0.1, 0.1],
        "NN_LAYERS": [512, 256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.03,
        "XGB_ESTIMATORS": 200,
        "XGB_MAX_DEPTH": 9,
        "XGB_SUBSAMPLE": 0.9,
        "XGB_COLSAMPLE_BYTREE": 0.9,
        "XGB_GAMMA": 0.4,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "none",
        "ACTIVATION": "leaky_relu"
    },
    
    # 17. Very High Capacity with Class Weights
    {
        "name": "Very_High_Capacity_Class_Weights",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 50,
        "TEST_SIZE": 0.1,
        "VAL_SIZE": 0.1,
        "NN_EPOCHS": 250,
        "NN_BATCH_SIZE": 16,
        "NN_LEARNING_RATE": 0.0003,
        "NN_L2_REG": 0.005,
        "NN_DROPOUT_RATES": [0.4, 0.3, 0.2, 0.1, 0.1],
        "NN_LAYERS": [512, 256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.03,
        "XGB_ESTIMATORS": 200,
        "XGB_MAX_DEPTH": 9,
        "XGB_SUBSAMPLE": 0.9,
        "XGB_COLSAMPLE_BYTREE": 0.9,
        "XGB_GAMMA": 0.4,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "none",  # Using class weights instead
        "USE_CLASS_WEIGHTS": True,
        "ACTIVATION": "leaky_relu"
    },
    
    # 18. Extreme Capacity Model (Highest Expected Accuracy)
    {
        "name": "Extreme_Capacity",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 60,
        "TEST_SIZE": 0.1,
        "VAL_SIZE": 0.1,
        "NN_EPOCHS": 300,
        "NN_BATCH_SIZE": 8,
        "NN_LEARNING_RATE": 0.0001,
        "NN_L2_REG": 0.008,
        "NN_DROPOUT_RATES": [0.5, 0.4, 0.3, 0.2, 0.1],
        "NN_LAYERS": [512, 256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.02,
        "XGB_ESTIMATORS": 300,
        "XGB_MAX_DEPTH": 10,
        "XGB_SUBSAMPLE": 0.95,
        "XGB_COLSAMPLE_BYTREE": 0.95,
        "XGB_GAMMA": 0.5,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 19. Extreme Capacity with Robust Scaling
    {
        "name": "Extreme_Capacity_Robust",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 60,
        "TEST_SIZE": 0.1,
        "VAL_SIZE": 0.1,
        "NN_EPOCHS": 300,
        "NN_BATCH_SIZE": 8,
        "NN_LEARNING_RATE": 0.0001,
        "NN_L2_REG": 0.008,
        "NN_DROPOUT_RATES": [0.5, 0.4, 0.3, 0.2, 0.1],
        "NN_LAYERS": [512, 256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.02,
        "XGB_ESTIMATORS": 300,
        "XGB_MAX_DEPTH": 10,
        "XGB_SUBSAMPLE": 0.95,
        "XGB_COLSAMPLE_BYTREE": 0.95,
        "XGB_GAMMA": 0.5,
        "PREPROCESSING_METHOD": "robust",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "ACTIVATION": "leaky_relu"
    },
    
    # 20. Extreme Capacity with All Techniques
    {
        "name": "Extreme_Capacity_All_Techniques",
        "MIN_SAMPLES_PER_CLASS": 5,
        "K_FEATURES": 60,
        "TEST_SIZE": 0.1,
        "VAL_SIZE": 0.1,
        "NN_EPOCHS": 300,
        "NN_BATCH_SIZE": 8,
        "NN_LEARNING_RATE": 0.0001,
        "NN_L2_REG": 0.008,
        "NN_DROPOUT_RATES": [0.5, 0.4, 0.3, 0.2, 0.1],
        "NN_LAYERS": [512, 256, 128, 64, 32],
        "XGB_LEARNING_RATE": 0.02,
        "XGB_ESTIMATORS": 300,
        "XGB_MAX_DEPTH": 10,
        "XGB_SUBSAMPLE": 0.95,
        "XGB_COLSAMPLE_BYTREE": 0.95,
        "XGB_GAMMA": 0.5,
        "PREPROCESSING_METHOD": "power",
        "FEATURE_SELECTION_METHOD": "mutual_info",
        "SAMPLING_METHOD": "adasyn",
        "USE_CLASS_WEIGHTS": True,
        "ACTIVATION": "leaky_relu"
    }
]

# Constants
DATASET_PATH = 'crop_dataset.csv'
TARGET_COLUMN = 'Crop'
RANDOM_STATE = 42

# Results storage
all_results = []

def setup_directories(config_name):
    """Create directories for this configuration's results."""
    # Create main results directory if it doesn't exist
    if not os.path.exists("all_results"):
        os.makedirs("all_results")
    
    # Create directory for this specific configuration
    config_dir = os.path.join("all_results", f"config_{config_name}")
    
    # Create subdirectories for this configuration
    model_dir = os.path.join(config_dir, "models")
    graph_dir = os.path.join(config_dir, "graphs")
    preprocessing_dir = os.path.join(config_dir, "preprocessing")
    
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(graph_dir, exist_ok=True)
    os.makedirs(preprocessing_dir, exist_ok=True)
    
    print(f"Created directories for configuration: {config_name}")
    return config_dir, model_dir, graph_dir, preprocessing_dir

def load_and_preprocess_data(min_samples_per_class):
    """Load and preprocess the dataset."""
    data = pd.read_csv(DATASET_PATH)
    
    # Filter classes with too few samples
    class_counts = data[TARGET_COLUMN].value_counts()
    valid_classes = class_counts[class_counts >= min_samples_per_class].index
    data = data[data[TARGET_COLUMN].isin(valid_classes)].copy()
    
    # Encode target
    label_encoder = LabelEncoder()
    data[TARGET_COLUMN] = label_encoder.fit_transform(data[TARGET_COLUMN])
    
    # Separate features and target
    X = data.drop(columns=[TARGET_COLUMN])
    y = data[TARGET_COLUMN].values
    
    return X, y, label_encoder

def select_features(X, y, k_features, method):
    """Select top k features using specified method."""
    if method == "mutual_info":
        selector = SelectKBest(score_func=mutual_info_classif, k=min(k_features, X.shape[1]))
    else:  # default to f_classif
        selector = SelectKBest(score_func=f_classif, k=min(k_features, X.shape[1]))
        
    X_selected = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()].tolist()
    
    return X_selected, selected_features, selector

def apply_preprocessing(X, method):
    """Apply specified preprocessing method."""
    if method == "power":
        preprocessor = PowerTransformer(method='yeo-johnson')
    elif method == "robust":
        preprocessor = RobustScaler()
    else:  # default to standard
        preprocessor = StandardScaler()
    
    X_processed = preprocessor.fit_transform(X)
    return X_processed, preprocessor

def handle_imbalance(X, y, method, random_state):
    """Handle class imbalance using specified method."""
    if method == "smote":
        sampler = SMOTE(random_state=random_state)
        X_res, y_res = sampler.fit_resample(X, y)
    elif method == "adasyn":
        sampler = ADASYN(random_state=random_state)
        X_res, y_res = sampler.fit_resample(X, y)
    elif method == "undersample":
        sampler = RandomUnderSampler(random_state=random_state)
        X_res, y_res = sampler.fit_resample(X, y)
    else:  # no sampling
        X_res, y_res = X, y
    
    return X_res, y_res

def calculate_class_weights(y):
    """Calculate class weights for imbalanced datasets."""
    class_counts = np.bincount(y)
    total_samples = len(y)
    n_classes = len(class_counts)
    
    weights = {}
    for class_idx in range(n_classes):
        weights[class_idx] = total_samples / (n_classes * class_counts[class_idx])
    
    return weights

def build_nn_model(input_shape, num_classes, dropout_rates, learning_rate, l2_reg, layers, activation):
    """Build a neural network model."""
    model = keras.Sequential()
    
    # Input layer
    model.add(Dense(layers[0], input_shape=input_shape, 
                   kernel_regularizer=l2(l2_reg)))
    
    if activation == "leaky_relu":
        model.add(LeakyReLU(alpha=0.01))
    else:
        model.add(keras.layers.Activation('relu'))
        
    model.add(Dropout(dropout_rates[0]))
    model.add(BatchNormalization())
    
    # Hidden layers
    for i, units in enumerate(layers[1:], 1):
        model.add(Dense(units, kernel_regularizer=l2(l2_reg)))
        
        if activation == "leaky_relu":
            model.add(LeakyReLU(alpha=0.01))
        else:
            model.add(keras.layers.Activation('relu'))
            
        if i < len(dropout_rates):
            model.add(Dropout(dropout_rates[i]))
        model.add(BatchNormalization())
    
    # Output layer
    model.add(Dense(num_classes, activation='softmax'))
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_nn_model(model, X_train, y_train, X_val, y_val, epochs, batch_size, class_weights=None):
    """Train the neural network model."""
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=10, min_lr=0.00001)
    ]
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )
    
    return history

def train_xgb_model(X_train, y_train, X_val, y_val, learning_rate, n_estimators, 
                   max_depth, subsample, colsample_bytree, gamma):
    """Train an XGBoost model."""
    model = xgb.XGBClassifier(
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        max_depth=max_depth,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        gamma=gamma,
        random_state=RANDOM_STATE,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        early_stopping_rounds=20,
        verbose=False
    )
    
    return model

def evaluate_model(model, X_test, y_test, model_name):
    """Evaluate model performance."""
    if hasattr(model, 'predict_proba'):
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)
    else:
        y_proba = model.predict(X_test)
        y_pred = np.argmax(y_proba, axis=1)
    
    accuracy = accuracy_score(y_test, y_pred)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    
    # Generate classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    weighted_precision = report['weighted avg']['precision']
    weighted_recall = report['weighted avg']['recall']
    weighted_f1 = report['weighted avg']['f1-score']
    
    print(f"{model_name} Accuracy: {accuracy:.4f}")
    print(f"{model_name} Balanced Accuracy: {balanced_acc:.4f}")
    print(f"{model_name} Weighted F1-score: {weighted_f1:.4f}")
    
    return y_pred, y_proba, accuracy, balanced_acc, weighted_precision, weighted_recall, weighted_f1

def plot_training_history(history, graph_dir, config_name):
    """Plot training history for neural network."""
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title(f'{config_name} - Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(f'{config_name} - Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'training_history.png'))
    plt.close()

def plot_confusion_matrix(y_true, y_pred, label_encoder, graph_dir, model_name):
    """Plot confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'{model_name} Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, f'{model_name}_confusion_matrix.png'))
    plt.close()

def plot_feature_importance(xgb_model, feature_names, graph_dir):
    """Plot feature importance for XGBoost."""
    importance_scores = xgb_model.feature_importances_
    indices = np.argsort(importance_scores)[::-1]
    
    # Plot top 20 features
    top_n = min(20, len(feature_names))
    plt.figure(figsize=(12, 8))
    plt.title('Feature Importance (Top 20)')
    plt.bar(range(top_n), importance_scores[indices][:top_n])
    plt.xticks(range(top_n), [feature_names[i] for i in indices[:top_n]], rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'feature_importance.png'))
    plt.close()

def plot_performance_comparison(nn_acc, xgb_acc, ensemble_acc, graph_dir):
    """Plot performance comparison between models."""
    models = ['Neural Network', 'XGBoost', 'Ensemble']
    accuracies = [nn_acc, xgb_acc, ensemble_acc]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(models, accuracies, color=['blue', 'green', 'red'])
    plt.title('Model Performance Comparison')
    plt.ylabel('Balanced Accuracy')
    plt.ylim(0, 1)
    
    # Add value labels on top of bars
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{acc:.4f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'performance_comparison.png'))
    plt.close()

def run_configuration(config, config_idx):
    """Run a single configuration."""
    print(f"\n{'='*60}")
    print(f"Running Configuration {config_idx+1}: {config['name']}")
    print(f"{'='*60}")
    
    # Setup directories for this configuration
    config_dir, model_dir, graph_dir, preprocessing_dir = setup_directories(config['name'])
    
    # Load and preprocess data
    X, y, label_encoder = load_and_preprocess_data(config['MIN_SAMPLES_PER_CLASS'])
    
    # Select features
    X_selected, selected_features, selector = select_features(
        X, y, config['K_FEATURES'], config['FEATURE_SELECTION_METHOD']
    )
    print(f"Selected {len(selected_features)} features using {config['FEATURE_SELECTION_METHOD']}")
    
    # Apply preprocessing
    X_processed, preprocessor = apply_preprocessing(X_selected, config['PREPROCESSING_METHOD'])
    print(f"Applied {config['PREPROCESSING_METHOD']} preprocessing")
    
    # Handle imbalance
    X_balanced, y_balanced = handle_imbalance(
        X_processed, y, config['SAMPLING_METHOD'], RANDOM_STATE
    )
    print(f"Applied {config['SAMPLING_METHOD']} for imbalance handling")
    
    # Calculate class weights if needed
    class_weights = None
    if config.get('USE_CLASS_WEIGHTS', False):
        class_weights = calculate_class_weights(y_balanced)
        print("Using class weights for training")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_balanced, y_balanced, test_size=config['TEST_SIZE'], 
        random_state=RANDOM_STATE, stratify=y_balanced
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=config['VAL_SIZE'], 
        random_state=RANDOM_STATE, stratify=y_train
    )
    
    # Train Neural Network
    print("Training Neural Network...")
    nn_model = build_nn_model(
        (X_train.shape[1],), 
        len(np.unique(y)), 
        config['NN_DROPOUT_RATES'], 
        config['NN_LEARNING_RATE'],
        config['NN_L2_REG'],
        config['NN_LAYERS'],
        config['ACTIVATION']
    )
    
    nn_history = train_nn_model(
        nn_model, X_train, y_train, X_val, y_val, 
        config['NN_EPOCHS'], config['NN_BATCH_SIZE'], class_weights
    )
    
    # Train XGBoost
    print("Training XGBoost...")
    xgb_model = train_xgb_model(
        X_train, y_train, X_val, y_val,
        config['XGB_LEARNING_RATE'], config['XGB_ESTIMATORS'], 
        config['XGB_MAX_DEPTH'], config['XGB_SUBSAMPLE'],
        config['XGB_COLSAMPLE_BYTREE'], config['XGB_GAMMA']
    )
    
    # Evaluate models
    print("Evaluating models...")
    nn_pred, nn_proba, nn_acc, nn_bal_acc, nn_prec, nn_rec, nn_f1 = evaluate_model(
        nn_model, X_test, y_test, "Neural Network"
    )
    xgb_pred, xgb_proba, xgb_acc, xgb_bal_acc, xgb_prec, xgb_rec, xgb_f1 = evaluate_model(
        xgb_model, X_test, y_test, "XGBoost"
    )
    
    # Create ensemble predictions (simple average)
    ensemble_proba = (nn_proba + xgb_proba) / 2
    ensemble_pred = np.argmax(ensemble_proba, axis=1)
    ensemble_acc = accuracy_score(y_test, ensemble_pred)
    ensemble_bal_acc = balanced_accuracy_score(y_test, ensemble_pred)
    
    # Calculate ensemble metrics
    report = classification_report(y_test, ensemble_pred, output_dict=True)
    ensemble_prec = report['weighted avg']['precision']
    ensemble_rec = report['weighted avg']['recall']
    ensemble_f1 = report['weighted avg']['f1-score']
    
    print(f"Ensemble Accuracy: {ensemble_acc:.4f}")
    print(f"Ensemble Balanced Accuracy: {ensemble_bal_acc:.4f}")
    print(f"Ensemble Weighted F1-score: {ensemble_f1:.4f}")
    
    # Determine best model
    best_model_type = "nn"
    best_accuracy = nn_bal_acc
    
    if xgb_bal_acc > best_accuracy:
        best_model_type = "xgb"
        best_accuracy = xgb_bal_acc
    
    if ensemble_bal_acc > best_accuracy:
        best_model_type = "ensemble"
        best_accuracy = ensemble_bal_acc
    
    print(f"Best model: {best_model_type} with balanced accuracy: {best_accuracy:.4f}")
    
    # Save plots to the configuration's graph directory
    print("Generating and saving plots...")
    plot_training_history(nn_history, graph_dir, config['name'])
    plot_confusion_matrix(y_test, nn_pred, label_encoder, graph_dir, "NN")
    plot_confusion_matrix(y_test, xgb_pred, label_encoder, graph_dir, "XGB")
    plot_confusion_matrix(y_test, ensemble_pred, label_encoder, graph_dir, "Ensemble")
    plot_feature_importance(xgb_model, selected_features, graph_dir)
    plot_performance_comparison(nn_bal_acc, xgb_bal_acc, ensemble_bal_acc, graph_dir)
    
    # Save models and preprocessing objects
    print("Saving models...")
    nn_model.save(os.path.join(model_dir, 'nn_model.h5'))
    joblib.dump(xgb_model, os.path.join(model_dir, 'xgb_model.joblib'))
    joblib.dump(preprocessor, os.path.join(preprocessing_dir, 'preprocessor.joblib'))
    joblib.dump(selector, os.path.join(preprocessing_dir, 'feature_selector.joblib'))
    np.save(os.path.join(preprocessing_dir, 'label_encoder_classes.npy'), label_encoder.classes_)
    
    # Save configuration details
    config_details = {
        "config_name": config['name'],
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "best_model": best_model_type,
        "nn_accuracy": nn_acc,
        "nn_balanced_accuracy": nn_bal_acc,
        "nn_precision": nn_prec,
        "nn_recall": nn_rec,
        "nn_f1": nn_f1,
        "xgb_accuracy": xgb_acc,
        "xgb_balanced_accuracy": xgb_bal_acc,
        "xgb_precision": xgb_prec,
        "xgb_recall": xgb_rec,
        "xgb_f1": xgb_f1,
        "ensemble_accuracy": ensemble_acc,
        "ensemble_balanced_accuracy": ensemble_bal_acc,
        "ensemble_precision": ensemble_prec,
        "ensemble_recall": ensemble_rec,
        "ensemble_f1": ensemble_f1,
        "selected_features": selected_features,
        "parameters": config
    }
    
    joblib.dump(config_details, os.path.join(config_dir, 'config_details.joblib'))
    
    # Store results for final comparison
    all_results.append({
        "config_name": config['name'],
        "nn_bal_acc": nn_bal_acc,
        "xgb_bal_acc": xgb_bal_acc,
        "ensemble_bal_acc": ensemble_bal_acc,
        "best_model": best_model_type,
        "config_dir": config_dir
    })
    
    return config_details

def generate_comparison_report():
    """Generate a comparison report of all configurations."""
    print("\n📊 Generating comparison report...")
    
    # Create comparison plot
    plt.figure(figsize=(16, 10))
    
    config_names = [result['config_name'] for result in all_results]
    nn_accs = [result['nn_bal_acc'] for result in all_results]
    xgb_accs = [result['xgb_bal_acc'] for result in all_results]
    ensemble_accs = [result['ensemble_bal_acc'] for result in all_results]
    
    x = np.arange(len(config_names))
    width = 0.25
    
    plt.bar(x - width, nn_accs, width, label='Neural Network')
    plt.bar(x, xgb_accs, width, label='XGBoost')
    plt.bar(x + width, ensemble_accs, width, label='Ensemble')
    
    plt.xlabel('Configuration')
    plt.ylabel('Balanced Accuracy')
    plt.title('Model Performance Comparison Across Configurations (Ordered by Expected Performance)')
    plt.xticks(x, config_names, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    # Save comparison plot in the main results directory
    plt.savefig(os.path.join("all_results", 'configuration_comparison.png'))
    plt.show()
    
    # Find best configuration
    best_idx = np.argmax([result['ensemble_bal_acc'] for result in all_results])
    best_config = all_results[best_idx]
    
    print(f"\n🏆 Best Configuration: {best_config['config_name']}")
    print(f"   Ensemble Balanced Accuracy: {best_config['ensemble_bal_acc']:.4f}")
    print(f"   Best Model Type: {best_config['best_model']}")
    print(f"   Results saved in: {best_config['config_dir']}")
    
    # Print detailed results table
    print("\n📋 Detailed Results:")
    print("-" * 120)
    print(f"{'Configuration':<30} {'NN Bal Acc':<12} {'XGB Bal Acc':<12} {'Ensemble Bal Acc':<15} {'Best Model':<10}")
    print("-" * 120)
    for result in all_results:
        print(f"{result['config_name']:<30} {result['nn_bal_acc']:<12.4f} {result['xgb_bal_acc']:<12.4f} {result['ensemble_bal_acc']:<15.4f} {result['best_model']:<10}")
    print("-" * 120)
    
    # Save detailed results to CSV
    results_df = pd.DataFrame(all_results)
    results_df.to_csv(os.path.join("all_results", 'detailed_results.csv'), index=False)
    print(f"Detailed results saved to: {os.path.join('all_results', 'detailed_results.csv')}")

def main():
    """Run all configurations sequentially."""
    print("Starting training with 20 different parameter configurations")
    print("Configurations are ordered from lowest to highest expected accuracy")
    
    # Run each configuration
    for i, config in enumerate(configurations):
        try:
            print(f"\n🚀 Processing configuration {i+1}/{len(configurations)}")
            result = run_configuration(config, i)
            print(f"✅ Completed: {config['name']}")
        except Exception as e:
            print(f"❌ Error in configuration {config['name']}: {str(e)}")
    
    # Generate comparison report
    generate_comparison_report()
    
    print("\n🎉 All 20 configurations completed!")
    print("All results have been saved in the 'all_results' directory")
    print("Each configuration has its own folder with models and graphs")

if __name__ == "__main__":
    # Install required packages if not already installed
    try:
        import xgboost as xgb
    except ImportError:
        print("Installing xgboost...")
        import subprocess
        subprocess.check_call(["pip", "install", "xgboost"])
        import xgboost as xgb
    
    try:
        from imblearn.over_sampling import SMOTE, ADASYN
        from imblearn.under_sampling import RandomUnderSampler
    except ImportError:
        print("Installing imbalanced-learn...")
        import subprocess
        subprocess.check_call(["pip", "install", "imbalanced-learn"])
        from imblearn.over_sampling import SMOTE, ADASYN
        from imblearn.under_sampling import RandomUnderSampler
    
    main()