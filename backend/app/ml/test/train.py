import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, PowerTransformer, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import accuracy_score, classification_report, balanced_accuracy_score
from sklearn.utils import class_weight
import xgboost as xgb
import os
import joblib

# --- Configuration Tweaks ---
K_FEATURES_TO_SELECT = 100
NN_LEARNING_RATE = 0.001
XGB_N_ESTIMATORS = 1000
XGB_EARLY_STOPPING_ROUNDS = 25

# --- Updated Neural Network Model ---
def build_nn_model(input_shape_val, num_classes_val, l2_reg, dropout_rates_list):
    inputs = keras.Input(shape=input_shape_val)
    x = Dense(512, kernel_initializer='he_normal', kernel_regularizer=keras.regularizers.l2(l2_reg))(inputs)
    x = tf.keras.layers.ReLU()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    x = Dense(256, kernel_initializer='he_normal', kernel_regularizer=keras.regularizers.l2(l2_reg))(x)
    x = tf.keras.layers.ReLU()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)

    x = Dense(128, kernel_initializer='he_normal', kernel_regularizer=keras.regularizers.l2(l2_reg))(x)
    x = tf.keras.layers.ReLU()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)

    outputs = Dense(num_classes_val, activation='softmax')(x)
    return keras.Model(inputs, outputs)

# --- Updated Training Function ---
def train_nn_model_func(nn_model_obj, X_train_data, y_train_data, X_val_data, y_val_data, epochs, batch_size, class_weights_map):
    print("\n🧠 Training Neural Network model...")
    opt = keras.optimizers.Adam(learning_rate=NN_LEARNING_RATE)
    nn_model_obj.compile(
        optimizer=opt,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )

    es = EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True, verbose=1)
    rlr = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=10, min_lr=1e-6, verbose=1)

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

# --- Enhanced Evaluation ---
def evaluate_model_performance(model, X_test_data, y_test_data, model_name="Model"):
    if hasattr(model, 'predict_proba'):
        preds_proba = model.predict_proba(X_test_data)
        pred_classes = np.argmax(preds_proba, axis=1)
    else:
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
        print("Per-class Precision/Recall/F1:")
        for cls, metrics in report.items():
            if cls not in ['accuracy', 'macro avg', 'weighted avg']:
                print(f"Class {cls} - Precision: {metrics['precision']:.2f}, Recall: {metrics['recall']:.2f}, F1: {metrics['f1-score']:.2f}")
    except Exception as e:
        print(f"Could not generate detailed metrics for {model_name}: {e}")
    return preds_proba, pred_classes, accuracy, balanced_accuracy
