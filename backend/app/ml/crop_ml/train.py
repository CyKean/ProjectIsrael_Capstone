import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder, PowerTransformer, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report, balanced_accuracy_score
from sklearn.utils import class_weight
import matplotlib.pyplot as plt
import os
import joblib
import io
import json # Added import
import seaborn as sns # Added import
from contextlib import redirect_stdout
from datetime import datetime

# --- Configuration ---
DATASET_PATH = 'crop_dataset.csv'
TARGET_COLUMN = 'Crop'
MIN_SAMPLES_PER_CLASS = 5
K_FEATURES_TO_SELECT = 35
TEST_SPLIT_SIZE = 0.2
VALIDATION_SPLIT_SIZE = 0.2 # Proportion of the (1 - TEST_SPLIT_SIZE) data

NN_EPOCHS = 250
NN_BATCH_SIZE = 32
NN_LEARNING_RATE = 0.0005
NN_L2_REG = 0.002
NN_DROPOUT_RATES = [0.4, 0.3, 0.2]

XGB_LEARNING_RATE = 0.02
XGB_N_ESTIMATORS = 500
XGB_MAX_DEPTH = 6
XGB_SUBSAMPLE = 0.8
XGB_COLSAMPLE_BYTREE = 0.8
XGB_GAMMA = 0.1
XGB_EARLY_STOPPING_ROUNDS = 10

RANDOM_STATE = 42

PREPROCESSING_DIR = 'preprocessing'
GRAPHS_DIR = 'graphs'
MODELS_DIR = 'models'

# --- Helper Functions ---

def setup_environment():
    """Creates necessary directories and sets random seeds."""
    os.makedirs(PREPROCESSING_DIR, exist_ok=True)
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    np.random.seed(RANDOM_STATE)
    tf.random.set_seed(RANDOM_STATE)
    print(f"🌱 Environment setup complete. Output directories: {PREPROCESSING_DIR}, {GRAPHS_DIR}, {MODELS_DIR}")

def load_and_filter_data(dataset_path, target_column, min_samples_per_class):
    """Loads the dataset and filters classes with insufficient samples."""
    data = pd.read_csv(dataset_path)
    print("Initial class distribution:")
    class_dist = data[target_column].value_counts()
    print(class_dist)
    print(f"Total samples: {len(data)}, Total classes: {len(class_dist)}")

    class_counts = data[target_column].value_counts()
    valid_classes = class_counts[class_counts >= min_samples_per_class].index
    excluded_classes_info = class_counts[class_counts < min_samples_per_class]

    if not excluded_classes_info.empty:
        print(f"\n⚠️ Excluding crops with < {min_samples_per_class} samples:\n{excluded_classes_info}")
        print(f"Number of excluded classes: {len(excluded_classes_info)}")

    data = data[data[target_column].isin(valid_classes)].copy()
    print(f"\nRemaining samples: {len(data)}, Remaining classes: {len(valid_classes)}")

    if len(valid_classes) < 2:
        print("\n❌ Error: Not enough classes with sufficient samples to perform classification. Exiting.")
        exit()
    return data, class_dist

def encode_target(data_df, target_column):
    """Encodes the target column and saves the encoder classes."""
    label_encoder = LabelEncoder()
    data_df[target_column] = label_encoder.fit_transform(data_df[target_column])
    np.save(os.path.join(PREPROCESSING_DIR, 'label_classes.npy'), label_encoder.classes_)
    num_classes_original_encoding = len(label_encoder.classes_)
    print(f"\n🏷️ Target column '{target_column}' encoded. Number of classes: {num_classes_original_encoding}")
    return data_df, label_encoder, num_classes_original_encoding

def engineer_features(df_X):
    """Creates interaction features from numerical columns."""
    numeric_cols = df_X.select_dtypes(include=np.number).columns.tolist()
    print(f"\n🛠️ Creating interaction features from: {numeric_cols}")
    X_eng = df_X.copy()
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            X_eng[f'{col1}_div_{col2}'] = X_eng[col1] / (X_eng[col2] + 1e-6)
            X_eng[f'{col1}_x_{col2}'] = X_eng[col1] * X_eng[col2]
            X_eng[f'{col1}_plus_{col2}'] = X_eng[col1] + X_eng[col2]
            X_eng[f'{col1}_minus_{col2}'] = X_eng[col1] - X_eng[col2]
    
    print(f"Features after interaction: {X_eng.shape[1]}")
    X_eng = pd.get_dummies(X_eng, dummy_na=False)
    print(f"Features after one-hot encoding (if any new categoricals arose): {X_eng.shape[1]}")
    return X_eng

def select_features_func(X_engineered, y_encoded_values, k_features_count):
    """Selects top k features using SelectKBest."""
    k_to_select = min(k_features_count, X_engineered.shape[1])
    selector = SelectKBest(score_func=f_classif, k=k_to_select)
    selector.fit_transform(X_engineered, y_encoded_values) # Fit to get mask
    selected_features_mask = selector.get_support()
    selected_feature_names_list = X_engineered.columns[selected_features_mask].tolist()

    print(f"\n🎯 Selected {len(selected_feature_names_list)} features for model training.")
    X_selected_df = X_engineered[selected_feature_names_list]
    np.save(os.path.join(PREPROCESSING_DIR, 'selected_feature_names.npy'), np.array(selected_feature_names_list, dtype=object))
    return X_selected_df, selected_feature_names_list

def preprocess_data_func(df_X_selected):
    """Applies PowerTransform and RobustScaler to features."""
    print("\n🔄 Preprocessing features (PowerTransform, RobustScale)...")
    df_X_processed = df_X_selected.copy()
    df_X_processed = df_X_processed.replace([np.inf, -np.inf], np.nan)
    if df_X_processed.isna().any().any():
        print(f"Found {df_X_processed.isna().sum().sum()} NaN values, filling with column median.")
        for col in df_X_processed.columns[df_X_processed.isna().any()]:
            df_X_processed[col] = df_X_processed[col].fillna(df_X_processed[col].median())
    if df_X_processed.isna().any().any():
        print(f"Found remaining {df_X_processed.isna().sum().sum()} NaN values after median fill, filling with 0.")
        df_X_processed = df_X_processed.fillna(0)

    pt = PowerTransformer(method='yeo-johnson', standardize=False)
    rs = RobustScaler()
    
    X_power = pt.fit_transform(df_X_processed)
    X_robust = rs.fit_transform(X_power)
    
    joblib.dump(pt, os.path.join(PREPROCESSING_DIR, 'power_transformer.joblib'))
    joblib.dump(rs, os.path.join(PREPROCESSING_DIR, 'robust_scaler.joblib'))
    print("✅ Preprocessing complete. Transformers saved.")
    return X_robust, pt, rs

def handle_imbalance(X_proc, y_enc, random_state_val):
    """Handles class imbalance using SMOTE or calculates class weights."""
    print("\n⚖️ Handling class imbalance...")
    print("Class distribution before resampling:")
    print(pd.Series(y_enc).value_counts().sort_index())

    min_class_count = pd.Series(y_enc).value_counts().min()
    num_unique_classes = len(np.unique(y_enc))
    calculated_class_weights = None
    X_res, y_res = X_proc, y_enc

    smote_min_samples_for_k5 = 6 # SMOTE's k_neighbors default is 5, needs k+1 samples
    # Condition for applying SMOTE: significant imbalance (e.g. min class < 50 samples) AND enough samples for SMOTE
    if min_class_count < 50 and num_unique_classes > 1 and min_class_count >= smote_min_samples_for_k5:
        print(f"Applying SMOTE. Smallest class has {min_class_count} samples.")
        smote_k = min(5, min_class_count - 1) # Adjust k_neighbors
        smote = SMOTE(random_state=random_state_val, k_neighbors=smote_k if smote_k > 0 else 1)
        X_res, y_res = smote.fit_resample(X_proc, y_enc)
        print("Class distribution after SMOTE:")
        print(pd.Series(y_res).value_counts().sort_index())
    else:
        if num_unique_classes > 1:
            if min_class_count < smote_min_samples_for_k5 :
                 print(f"Skipping SMOTE: smallest class ({min_class_count} samples) is too small for default k_neighbors.")
            else:
                 print("Skipping SMOTE: classes seem relatively balanced or not meeting SMOTE criteria.")
            weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_res), y=y_res)
            calculated_class_weights = dict(enumerate(weights))
            print("Calculated class weights for NN model as SMOTE was not applied.")
    return X_res, y_res, calculated_class_weights

def split_data_func(X_input, y_input, test_size, val_size, random_state_val):
    """Splits data into training, validation, and test sets."""
    print("\n📊 Splitting data...")
    final_counts = pd.Series(y_input).value_counts()
    stratify_tts = y_input if final_counts.min() >= 2 else None

    X_train_val_data, X_test_data, y_train_val_data, y_test_data = train_test_split(
        X_input, y_input, test_size=test_size, random_state=random_state_val, stratify=stratify_tts
    )

    train_val_counts = pd.Series(y_train_val_data).value_counts()
    stratify_tv = y_train_val_data if train_val_counts.min() >= 2 else None

    X_train_data, X_val_data, y_train_data, y_val_data = train_test_split(
        X_train_val_data, y_train_val_data, test_size=val_size, random_state=random_state_val, stratify=stratify_tv
    )
    print(f"Training set: {X_train_data.shape[0]} samples, {X_train_data.shape[1]} features")
    print(f"Validation set: {X_val_data.shape[0]} samples")
    print(f"Test set: {X_test_data.shape[0]} samples")
    return X_train_data, X_val_data, X_test_data, y_train_data, y_val_data, y_test_data

def build_nn_model(input_shape_val, num_classes_val, l2_reg, dropout_rates_list):
    """Builds the Keras Neural Network model."""
    inputs = keras.Input(shape=input_shape_val)
    x = Dense(256, kernel_regularizer=keras.regularizers.l2(l2_reg))(inputs)
    x = LeakyReLU(negative_slope=0.01)(x) # Updated parameter
    x = BatchNormalization()(x) # BatchNormalization helps with higher learning rates and regularization
    x = Dropout(dropout_rates_list[0])(x)

    x = Dense(128, kernel_regularizer=keras.regularizers.l2(l2_reg))(x)
    x = LeakyReLU(negative_slope=0.01)(x) # Updated parameter
    x = BatchNormalization()(x)
    x = Dropout(dropout_rates_list[1])(x)

    x = Dense(64, kernel_regularizer=keras.regularizers.l2(l2_reg))(x)
    x = LeakyReLU(negative_slope=0.01)(x) # Updated parameter
    x = BatchNormalization()(x)
    x = Dropout(dropout_rates_list[2])(x)
    
    outputs = Dense(num_classes_val, activation='softmax')(x)
    model = keras.Model(inputs, outputs)
    return model

def train_nn_model_func(nn_model_obj, X_train_data, y_train_data, X_val_data, y_val_data, epochs, batch_size, class_weights_map):
    """Compiles and trains the Neural Network model."""
    print("\n🧠 Training Neural Network model...")
    opt = keras.optimizers.Adam(learning_rate=NN_LEARNING_RATE)
    nn_model_obj.compile(
        optimizer=opt,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )

    es = EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True, verbose=1)
    rlr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=15, min_lr=0.00001, verbose=1)

    train_params = {
        'validation_data': (X_val_data, y_val_data),
        'epochs': epochs,
        'batch_size': batch_size,
        'callbacks': [es, rlr],
        'verbose': 1
    }
    if class_weights_map:
        train_params['class_weight'] = class_weights_map
        print("Using class weights for NN training.")

    history = nn_model_obj.fit(X_train_data, y_train_data, **train_params)
    print("✅ Neural Network training complete.")
    return history

def build_and_train_xgb_model_func(X_train_data, y_train_data, X_val_data, y_val_data, num_classes_val, random_state_val):
    """Builds and trains the XGBoost model."""
    print("\n🌲 Training XGBoost model...")
    xgb_model_obj = xgb.XGBClassifier(
        learning_rate=XGB_LEARNING_RATE,
        n_estimators=XGB_N_ESTIMATORS,
        max_depth=XGB_MAX_DEPTH,
        objective='multi:softprob',
        num_class=num_classes_val,
        random_state=random_state_val,
        use_label_encoder=False,
        eval_metric='mlogloss',
        subsample=XGB_SUBSAMPLE,
        colsample_bytree=XGB_COLSAMPLE_BYTREE,
        gamma=XGB_GAMMA
    )
    try:
        xgb_model_obj.fit(X_train_data, y_train_data,
                      eval_set=[(X_val_data, y_val_data)],
                      early_stopping_rounds=XGB_EARLY_STOPPING_ROUNDS, # Correctly in fit() for scikit-learn wrapper
                      verbose=False)
        print("✅ XGBoost model training completed.")
        return xgb_model_obj
    except Exception as e:
        print(f"❌ XGBoost training failed: {e}")
        return None

def evaluate_model_performance(model, X_test_data, y_test_data, model_name="Model"):
    """Evaluates the model and prints performance metrics."""
    if hasattr(model, 'predict_proba'): # XGBoost or similar
        preds_proba = model.predict_proba(X_test_data)
        pred_classes = np.argmax(preds_proba, axis=1)
    else: # Keras model
        preds_proba = model.predict(X_test_data)
        pred_classes = np.argmax(preds_proba, axis=1)
    
    accuracy = accuracy_score(y_test_data, pred_classes)
    balanced_accuracy = balanced_accuracy_score(y_test_data, pred_classes)
    print(f"\n{model_name} Test Accuracy: {accuracy:.4f}")
    print(f"{model_name} Balanced Test Accuracy: {balanced_accuracy:.4f}")

    try:
        report = classification_report(y_test_data, pred_classes, output_dict=True, zero_division=0)
        print(f"{model_name} Classification Report:")
        print(f"  Weighted Precision: {report['weighted avg']['precision']:.4f}")
        print(f"  Weighted Recall: {report['weighted avg']['recall']:.4f}")
        print(f"  Weighted F1-score: {report['weighted avg']['f1-score']:.4f}")
    except Exception as e:
        print(f"Could not generate detailed metrics for {model_name}: {e}")
    return preds_proba, pred_classes, accuracy, balanced_accuracy

def create_ensemble_predictions(nn_probs, xgb_probs, y_test_data):
    """Creates ensemble predictions and evaluates them."""
    print("\n🤝 Creating ensemble model (NN + XGBoost)...")
    ensemble_proba_val = (0.5 * nn_probs + 0.5 * xgb_probs)
    ensemble_preds_val = np.argmax(ensemble_proba_val, axis=1)
    ensemble_accuracy_val = accuracy_score(y_test_data, ensemble_preds_val)
    balanced_ensemble_accuracy_val = balanced_accuracy_score(y_test_data, ensemble_preds_val)
    print(f"Ensemble Test Accuracy: {ensemble_accuracy_val:.4f}")
    print(f"Ensemble Balanced Test Accuracy: {balanced_ensemble_accuracy_val:.4f}")

    try:
        report = classification_report(y_test_data, ensemble_preds_val, output_dict=True, zero_division=0)
        print("Ensemble Classification Report:")
        print(f"  Weighted Precision: {report['weighted avg']['precision']:.4f}")
        print(f"  Weighted Recall: {report['weighted avg']['recall']:.4f}")
        print(f"  Weighted F1-score: {report['weighted avg']['f1-score']:.4f}")
    except Exception as e:
        print(f"Could not generate detailed metrics for Ensemble: {e}")
    return ensemble_preds_val, ensemble_accuracy_val, balanced_ensemble_accuracy_val

def determine_best_model_type(nn_bal_acc, xgb_bal_acc, ens_bal_acc, xgb_model_obj):
    """Determines the best model based on balanced accuracy."""
    print("\n🏆 Determining best model...")
    model_scores = {"nn": nn_bal_acc}
    if xgb_model_obj:
        model_scores["xgb"] = xgb_bal_acc
        if ens_bal_acc > 0: # Ens_bal_acc will be 0 if xgb_model is None
            model_scores["ensemble"] = ens_bal_acc

    if not model_scores:
        final_best_model_type = "nn" # Should not happen
    else:
        final_best_model_type = max(model_scores, key=model_scores.get)
    
    print(f"Best performing model type: {final_best_model_type.upper()} with Balanced Accuracy {model_scores.get(final_best_model_type, 0.0):.4f}")
    return final_best_model_type

def save_training_artifacts(nn_model_obj, xgb_model_obj, best_model_type_val, nn_history_obj, 
                            y_test_data, nn_pred_classes_val, xgb_pred_classes_val, ensemble_preds_val,
                            num_classes_for_model_val, label_encoder_obj):
    """Saves models, plots, and other training artifacts."""
    print("\n💾 Saving models and artifacts...")
    nn_model_obj.save(os.path.join(MODELS_DIR, 'crop_nn_model.keras'))
    print("✅ Neural Network model saved.")

    if xgb_model_obj:
        joblib.dump(xgb_model_obj, os.path.join(MODELS_DIR, 'crop_xgb_model.joblib'))
        print("✅ XGBoost model saved.")

    with open(os.path.join(MODELS_DIR, 'best_model.txt'), 'w') as f:
        f.write(best_model_type_val)
    print(f"✅ Best model type ({best_model_type_val}) saved.")

    with open(os.path.join(MODELS_DIR, 'model_architecture.json'), 'w') as f:
        f.write(nn_model_obj.to_json())
    print("✅ NN model architecture saved.")

    # Save NN training plots
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(nn_history_obj.history['accuracy'], label='Training Accuracy')
    plt.plot(nn_history_obj.history['val_accuracy'], label='Validation Accuracy')
    plt.title('NN Model Accuracy')
    plt.xlabel('Epochs'); plt.ylabel('Accuracy'); plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(nn_history_obj.history['loss'], label='Training Loss')
    plt.plot(nn_history_obj.history['val_loss'], label='Validation Loss')
    plt.title('NN Model Loss')
    plt.xlabel('Epochs'); plt.ylabel('Loss'); plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, 'nn_model_performance.png'))
    plt.close()
    print("✅ NN performance plots saved.")

    # Save confusion matrix for the best model
    cm_preds = nn_pred_classes_val
    if best_model_type_val == "xgb" and xgb_model_obj:
        cm_preds = xgb_pred_classes_val
    elif best_model_type_val == "ensemble" and xgb_model_obj:
        cm_preds = ensemble_preds_val
    
    try:
        cm = confusion_matrix(y_test_data, cm_preds)
        if num_classes_for_model_val > 20:
            np.savetxt(os.path.join(GRAPHS_DIR, 'confusion_matrix.csv'), cm, delimiter=',', fmt='%d')
        else:
            plt.figure(figsize=(max(10, num_classes_for_model_val // 2), max(8, num_classes_for_model_val // 2.5)))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                        xticklabels=label_encoder_obj.classes_, yticklabels=label_encoder_obj.classes_)
            plt.title(f'Confusion Matrix ({best_model_type_val.upper()})')
            plt.ylabel('True Label'); plt.xlabel('Predicted Label'); plt.tight_layout()
            plt.savefig(os.path.join(GRAPHS_DIR, 'confusion_matrix.png'))
            plt.close()
        print("✅ Confusion matrix saved.")
    except Exception as e:
        print(f"Could not generate confusion matrix: {e}")

# --- Saving Models and Artifacts ---
# --- Prediction Function Saving ---
def generate_prediction_script_file(original_features_list_val, target_column_val):
    """Generates the standalone prediction_function.py script."""
    print("\n⚙️ Generating prediction_function.py...")
    # Get original feature names before engineering for the prediction function's docstring/guidance
    # original_feature_names_list = pd.read_csv(DATASET_PATH).drop(columns=[target_column_val]).columns.tolist()

    prediction_code = f"""
import pandas as pd
import numpy as np
import joblib
import os
import tensorflow as tf
from tensorflow import keras # Required for custom layers like LeakyReLU if used directly

# --- Define Paths ---
SCRIPT_DIR = os.path.dirname(__file__) # Assumes script is run from its location
PREPROCESSING_DIR_PRED = os.path.join(SCRIPT_DIR, '{PREPROCESSING_DIR}')
MODELS_DIR_PRED = os.path.join(SCRIPT_DIR, '{MODELS_DIR}')

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
        print(f"Warning: Could not load XGBoost model: {{e}}")

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
            X_eng[f'{{col1}}_div_{{col2}}'] = X_eng[col1] / (X_eng[col2] + 1e-6)
            X_eng[f'{{col1}}_x_{{col2}}'] = X_eng[col1] * X_eng[col2]
            X_eng[f'{{col1}}_plus_{{col2}}'] = X_eng[col1] + X_eng[col2]
            X_eng[f'{{col1}}_minus_{{col2}}'] = X_eng[col1] - X_eng[col2]
    return X_eng

# --- Prediction Function ---
def predict_crop(features_dict):
    \"\"\"
    Make a prediction for crop recommendation.
    
    Args:
        features_dict: Dictionary with keys for {original_features_list_val}
        
    Returns:
        Dictionary with 'crop', 'confidence', and 'all_crop_probabilities'
    \"\"\"
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
             print(f"Warning: NN and XGBoost models have inconsistent output shapes (NN: {{len(nn_probs_single)}}, XGB: {{len(xgb_probs_single)}}). Attempting to align for ensemble.")
             # A more robust solution might involve re-training one of the models or aligning classes explicitly.
        probabilities = (0.5 * nn_probs_single + 0.5 * xgb_probs_single) # Consistent 0.5/0.5 weights
    elif best_model_type == "xgb" and have_xgb:
        probabilities = xgb_model.predict_proba(input_robust)[0]
    else: # Default to NN or if XGB failed/not chosen
        probabilities = nn_model.predict(input_robust)[0]
        
    predicted_class_idx = np.argmax(probabilities)
    confidence = float(probabilities[predicted_class_idx])
    predicted_crop = label_encoder_classes[predicted_class_idx]

    all_crop_probabilities = {{
        label_encoder_classes[i]: float(probabilities[i]) 
        for i in range(len(probabilities))
    }}
    
    return {{
        'crop': predicted_crop,
        'confidence': confidence,
        'class_idx': int(predicted_class_idx),
        'all_crop_probabilities': all_crop_probabilities
    }}

if __name__ == '__main__':
    # Example usage:
    # Ensure your feature names match exactly those in 'original_feature_names_list'
    # These are the features BEFORE any engineering.
    example_features = {{
        '{original_features_list_val[0] if len(original_features_list_val) > 0 else "feature_1"}': 100, 
        '{original_features_list_val[1] if len(original_features_list_val) > 1 else "feature_2"}': 50, 
        '{original_features_list_val[2] if len(original_features_list_val) > 2 else "feature_3"}': 50, 
        # Add more features as per your original dataset
        # '{original_features_list_val[3]}': 25, 
        # '{original_features_list_val[4]}': 70, 
        # '{original_features_list_val[5]}': 6.5, 
        # '{original_features_list_val[6]}': 60
    }}
    # Fill remaining original features with a default value (e.g., 0 or mean) if not provided in the example
    all_original_features = {original_features_list_val}
    for feat_name in all_original_features:
        if feat_name not in example_features:
            example_features[feat_name] = 0 # Or a typical/mean value

    prediction = predict_crop(example_features)
    print(f"\nExample Prediction:")
    print(f"  Predicted Crop: {{prediction.get('crop', 'N/A')}}")
    print(f"  Confidence: {{prediction.get('confidence', 0.0):.4f}}")
    # print(f"  All Probabilities: {{prediction.get('all_crop_probabilities', {{}})}}")

"""
    with open('prediction_function.py', 'w', encoding='utf-8') as f:
        f.write(prediction_code)
    print("✅ Prediction function saved to 'prediction_function.py'")

def generate_summary_file_func(dataset_path_val, target_column_val, initial_class_dist,
                               min_samples_val, filtered_data_len, num_classes_orig_encoding,
                               y_resampled_len, X_engineered_shape, selected_features_names_list,
                               nn_model_obj, nn_history_obj, nn_bal_acc_val, xgb_model_obj, xgb_bal_acc_val,
                               ensemble_bal_acc_val, best_model_type_val):
    """Generates a summary text file of the training process."""
    print("\n📝 Generating training_summary.txt...")
    with open('training_summary.txt', 'w', encoding='utf-8') as f:
        f.write(f"Crop Classification Model Training Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("======================================================================\n\n")
        f.write(f"Dataset Information:\n")
        f.write(f"- Dataset Path: {dataset_path_val}\n")
        f.write(f"- Target Column: {target_column_val}\n")
        f.write(f"- Initial total samples: {initial_class_dist.sum()}, Initial classes: {len(initial_class_dist)}\n")
        f.write(f"- Min samples per class filter: {min_samples_val}\n")
        f.write(f"- Samples after filtering: {filtered_data_len}\n")
        f.write(f"- Classes after filtering (used for model output): {num_classes_orig_encoding}\n")
        f.write(f"- Samples after resampling (if any): {y_resampled_len}\n\n")
        
        f.write(f"Feature Engineering & Selection:\n")
        f.write(f"- Number of features after engineering: {X_engineered_shape[1]}\n")
        f.write(f"- Number of selected features for model: {len(selected_features_names_list)}\n\n")

        f.write(f"Model Architecture (Neural Network):\n")
        summary_str_io = io.StringIO()
        with redirect_stdout(summary_str_io):
            nn_model_obj.summary()
        f.write(summary_str_io.getvalue())
        
        f.write(f"\nTraining Performance (Balanced Accuracy on Test Set):\n")
        if nn_history_obj:
            f.write(f"- Neural Network Balanced Accuracy: {nn_bal_acc_val:.4f}\n")
            f.write(f"- Neural Network Best Validation Accuracy (raw): {max(nn_history_obj.history['val_accuracy']):.4f}\n")
            f.write(f"- Neural Network Best Validation Loss: {min(nn_history_obj.history['val_loss']):.4f}\n")
        
        if xgb_model_obj:
            f.write(f"- XGBoost Balanced Accuracy: {xgb_bal_acc_val:.4f}\n")
        
        if xgb_model_obj and ensemble_bal_acc_val > 0:
            f.write(f"- Ensemble Balanced Accuracy: {ensemble_bal_acc_val:.4f}\n")
        
        f.write(f"\n- Best Model Type (based on Balanced Accuracy): {best_model_type_val.upper()}\n")

        f.write(f"\nSelected Features ({len(selected_features_names_list)}):\n")
        for i, feature_name in enumerate(selected_features_names_list, 1):
            f.write(f"{i}. {feature_name}\n")
    print("✅ Training summary saved to 'training_summary.txt'")

# --- Main Execution ---
def main():
    setup_environment()

    # 1. Load and Filter Data
    data, initial_class_distribution = load_and_filter_data(DATASET_PATH, TARGET_COLUMN, MIN_SAMPLES_PER_CLASS)
    original_feature_names = data.drop(columns=[TARGET_COLUMN]).columns.tolist() # Get before encoding

    # 2. Encode Target
    data, label_encoder, num_classes_original_encoding = encode_target(data, TARGET_COLUMN)
    X = data.drop(columns=[TARGET_COLUMN])
    y_encoded = data[TARGET_COLUMN].values

    # 3. Feature Engineering
    X_engineered = engineer_features(X)

    # 4. Feature Selection
    X_selected, selected_feature_names = select_features_func(X_engineered, y_encoded, K_FEATURES_TO_SELECT)

    # 5. Preprocessing
    X_processed, power_transformer, robust_scaler = preprocess_data_func(X_selected)

    # 6. Handle Imbalance
    X_resampled, y_resampled, class_weights_dict = handle_imbalance(X_processed, y_encoded, RANDOM_STATE)

    # 7. Split Data
    X_train, X_val, X_test, y_train, y_val, y_test = split_data_func(
        X_resampled, y_resampled, TEST_SPLIT_SIZE, VALIDATION_SPLIT_SIZE, RANDOM_STATE
    )

    # Determine model input shape and number of classes
    input_shape = (X_train.shape[1],)
    num_classes_for_model = num_classes_original_encoding # Crucial: model output must match original encoding
    print(f"\nModel Configuration: Input Shape={input_shape}, Num Classes={num_classes_for_model}")

    # 8. Neural Network Training
    nn_model = build_nn_model(input_shape, num_classes_for_model, NN_L2_REG, NN_DROPOUT_RATES)
    nn_history = train_nn_model_func(nn_model, X_train, y_train, X_val, y_val, NN_EPOCHS, NN_BATCH_SIZE, class_weights_dict)

    # 9. XGBoost Training
    xgb_model = build_and_train_xgb_model_func(X_train, y_train, X_val, y_val, num_classes_for_model, RANDOM_STATE)

    # 10. Evaluation
    print("\n📊 Evaluating models on the Test Set...")
    nn_preds_proba, nn_pred_classes, nn_accuracy, nn_balanced_accuracy = evaluate_model_performance(
        nn_model, X_test, y_test, "Neural Network"
    )

    xgb_preds_proba, xgb_pred_classes, xgb_accuracy, xgb_balanced_accuracy = (None, None, 0.0, 0.0)
    if xgb_model:
        xgb_preds_proba, xgb_pred_classes, xgb_accuracy, xgb_balanced_accuracy = evaluate_model_performance(
            xgb_model, X_test, y_test, "XGBoost"
        )

    # 11. Ensemble
    ensemble_preds, ensemble_accuracy, ensemble_balanced_accuracy = (None, 0.0, 0.0)
    if xgb_model and nn_preds_proba is not None and xgb_preds_proba is not None:
        ensemble_preds, ensemble_accuracy, ensemble_balanced_accuracy = create_ensemble_predictions(
            nn_preds_proba, xgb_preds_proba, y_test
        )

    # 12. Determine Best Model
    best_model_type = determine_best_model_type(
        nn_balanced_accuracy, xgb_balanced_accuracy, ensemble_balanced_accuracy, xgb_model
    )

    # 13. Save Artifacts
    save_training_artifacts(nn_model, xgb_model, best_model_type, nn_history,
                            y_test, nn_pred_classes, xgb_pred_classes, ensemble_preds,
                            num_classes_for_model, label_encoder)

    # 14. Generate Prediction Script
    generate_prediction_script_file(original_feature_names, TARGET_COLUMN)

    # 15. Generate Summary File
    generate_summary_file_func(DATASET_PATH, TARGET_COLUMN, initial_class_distribution,
                               MIN_SAMPLES_PER_CLASS, len(data), num_classes_original_encoding,
                               len(y_resampled), X_engineered.shape, selected_feature_names,
                               nn_model, nn_history, nn_balanced_accuracy, xgb_model, xgb_balanced_accuracy,
                               ensemble_balanced_accuracy, best_model_type)

    print("\n🎉 Training pipeline completed successfully!")
    print_deployment_recommendations()

# --- Training Summary ---
def print_deployment_recommendations():
    """Prints recommendations for deploying the trained models."""
    print("\n=== RECOMMENDATIONS FOR DEPLOYMENT ===")
    print(f"1. Use the saved models in the '{MODELS_DIR}' directory: 'crop_nn_model.keras' and (if available) 'crop_xgb_model.joblib'.")
    print(f"2. The '{os.path.join(MODELS_DIR, 'best_model.txt')}' file indicates which model performed best (based on Balanced Accuracy).")
    print("3. Use 'prediction_function.py' for making new predictions. It's configured to use the best model and necessary preprocessors.")
    print(f"4. Ensure all preprocessing objects in the '{PREPROCESSING_DIR}' directory are co-located with 'prediction_function.py' and models for it to work.")
    print("5. For classes with few samples, monitor their prediction performance. If unsatisfactory, consider collecting more data or exploring advanced techniques like few-shot learning.")
    print("6. Periodically retrain the model with new, representative data to maintain and improve its performance over time.")

if __name__ == "__main__":
    main()
