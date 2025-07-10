#========================================================================================#

# maataas ang accuracy nito HAHAHAHAHHA nice one pakwan

# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
# from sklearn.model_selection import train_test_split, KFold
# from sklearn.preprocessing import StandardScaler, LabelEncoder, PowerTransformer, RobustScaler
# from sklearn.ensemble import VotingClassifier
# from sklearn.feature_selection import SelectKBest, f_classif
# from imblearn.over_sampling import SMOTE
# from imblearn.combine import SMOTEENN
# import xgboost as xgb
# from sklearn.metrics import accuracy_score
# import numpy as np

# # Load data
# data = pd.read_csv('crop_dataset_fixed.csv')
# target_column = 'Crop'

# # Separate features and labels
# X = data.drop(columns=[target_column])
# y = data[target_column]

# # Enhanced feature engineering
# def create_interaction_features(X):
#     numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
#     for i in range(len(numeric_cols)):
#         for j in range(i+1, len(numeric_cols)):
#             col1, col2 = numeric_cols[i], numeric_cols[j]
#             X[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-6)
#             X[f'{col1}_{col2}_product'] = X[col1] * X[col2]
#     return X

# # Apply feature engineering
# X = create_interaction_features(X)

# # Categorical encoding
# categorical_cols = X.select_dtypes(include=['object']).columns
# X = pd.get_dummies(X, columns=categorical_cols)

# # Feature selection
# selector = SelectKBest(score_func=f_classif, k='all')
# X_selected = selector.fit_transform(X, y)
# selected_features_mask = selector.get_support()
# selected_feature_names = X.columns[selected_features_mask].tolist()
# X = X[selected_feature_names]

# # Advanced preprocessing
# def preprocess_features(X):
#     power_transformer = PowerTransformer(method='yeo-johnson')
#     robust_scaler = RobustScaler()
    
#     # Apply both transformers
#     X_power = power_transformer.fit_transform(X)
#     X_robust = robust_scaler.fit_transform(X_power)
    
#     return X_robust

# X = preprocess_features(X)

# # Enhanced sampling
# smote_enn = SMOTEENN(random_state=42)
# X_resampled, y_resampled = smote_enn.fit_resample(X, y)

# # Label encoding
# label_encoder = LabelEncoder()
# y_encoded = label_encoder.fit_transform(y_resampled)

# # Define deep learning model
# def create_deep_model(input_shape, num_classes):
#     inputs = keras.Input(shape=input_shape)
    
#     # First block with skip connection
#     x = Dense(512, kernel_regularizer=keras.regularizers.l2(0.01))(inputs)
#     x = LeakyReLU(negative_slope=0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.5)(x)
    
#     skip1 = x
    
#     # Second block
#     x = Dense(256, kernel_regularizer=keras.regularizers.l2(0.01))(x)
#     x = LeakyReLU(negative_slope=0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.4)(x)
    
#     # Add skip connection
#     x = keras.layers.Concatenate()([x, skip1])
    
#     # Third block
#     x = Dense(128, kernel_regularizer=keras.regularizers.l2(0.01))(x)
#     x = LeakyReLU(negative_slope=0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.3)(x)
    
#     # Output
#     outputs = Dense(num_classes, activation='softmax')(x)
    
#     return keras.Model(inputs, outputs)

# # Create ensemble of models
# def create_ensemble(input_shape, num_classes, n_models=3):
#     models = []
    
#     for i in range(n_models):
#         # Deep learning model
#         dl_model = create_deep_model(input_shape, num_classes)
#         dl_model.compile(
#             optimizer=keras.optimizers.Adam(learning_rate=0.001),
#             loss='sparse_categorical_crossentropy',
#             metrics=['accuracy']
#         )
#         models.append(dl_model)
        
#         # XGBoost model
#         xgb_model = xgb.XGBClassifier(
#             learning_rate=0.01,
#             n_estimators=200,
#             max_depth=7,
#             min_child_weight=1,
#             gamma=0.1,
#             subsample=0.8,
#             colsample_bytree=0.8,
#             objective='multi:softprob',
#             num_class=num_classes,
#             random_state=42+i
#         )
#         models.append(xgb_model)
    
#     return models

# # Training with k-fold cross validation
# n_splits = 5
# kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

# # Callbacks for deep learning models
# early_stopping = EarlyStopping(
#     monitor='val_accuracy',
#     patience=20,
#     restore_best_weights=True,
#     min_delta=0.001
# )

# reduce_lr = ReduceLROnPlateau(
#     monitor='val_accuracy',
#     factor=0.2,
#     patience=10,
#     min_lr=1e-6,
#     min_delta=0.001,
#     verbose=1
# )

# # Train ensemble
# def train_ensemble(X, y, input_shape, num_classes):
#     ensemble_predictions = []
#     fold_accuracies = []
    
#     for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
#         print(f"\nTraining Fold {fold + 1}/{n_splits}")
        
#         X_train, X_val = X[train_idx], X[val_idx]
#         y_train, y_val = y[train_idx], y[val_idx]
        
#         # Create and train models for this fold
#         models = create_ensemble(input_shape, num_classes)
#         fold_predictions = []
        
#         for i, model in enumerate(models):
#             if isinstance(model, keras.Model):
#                 # Train deep learning model
#                 model.fit(
#                     X_train, y_train,
#                     validation_data=(X_val, y_val),
#                     epochs=100,
#                     batch_size=32,
#                     callbacks=[early_stopping, reduce_lr],
#                     verbose=1
#                 )
#                 pred = model.predict(X_val)
#                 fold_predictions.append(pred)
#             else:
#                 # Train XGBoost model
#                 model.fit(X_train, y_train)
#                 pred = model.predict_proba(X_val)
#                 fold_predictions.append(pred)
        
#         # Average predictions for this fold
#         fold_pred = np.mean(fold_predictions, axis=0)
#         fold_pred_classes = np.argmax(fold_pred, axis=1)
#         fold_accuracy = accuracy_score(y_val, fold_pred_classes)
#         fold_accuracies.append(fold_accuracy)
#         print(f"Fold {fold + 1} Accuracy: {fold_accuracy:.4f}")
        
#         ensemble_predictions.append((val_idx, fold_pred))
    
#     return ensemble_predictions, np.mean(fold_accuracies)

# # Train the ensemble
# input_shape = (X_resampled.shape[1],)
# num_classes = len(np.unique(y_encoded))
# ensemble_predictions, mean_accuracy = train_ensemble(X_resampled, y_encoded, input_shape, num_classes)

# print(f"\nMean Cross-Validation Accuracy: {mean_accuracy:.4f}")

# # Save predictions and actual values
# final_predictions = np.zeros((len(X_resampled), num_classes))
# for idx, pred in ensemble_predictions:
#     final_predictions[idx] = pred

# # Final evaluation
# final_pred_classes = np.argmax(final_predictions, axis=1)
# final_accuracy = accuracy_score(y_encoded, final_pred_classes)
# print(f"Final Ensemble Accuracy: {final_accuracy:.4f}")

# # Save the best model from the ensemble
# best_model = create_deep_model(input_shape, num_classes)
# best_model.compile(
#     optimizer=keras.optimizers.Adam(learning_rate=0.001),
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# best_model.fit(
#     X_resampled, y_encoded,
#     epochs=100,
#     batch_size=32,
#     callbacks=[early_stopping, reduce_lr],
#     validation_split=0.2,
#     verbose=1
# )
# best_model.save('best_crop_model.keras')








# from sklearn.preprocessing import PowerTransformer, RobustScaler
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
# from tensorflow.keras.callbacks import EarlyStopping
# from sklearn.model_selection import StratifiedKFold
# from sklearn.preprocessing import LabelEncoder
# from sklearn.feature_selection import SelectKBest, f_classif
# from imblearn.combine import SMOTEENN
# import xgboost as xgb
# from sklearn.metrics import accuracy_score

# # Load data
# data = pd.read_csv('crop_dataset_fixed.csv')
# target_column = 'Crop'

# # Separate features and labels
# X = data.drop(columns=[target_column])
# y = data[target_column]

# # Label encoding
# label_encoder = LabelEncoder()
# y_encoded = label_encoder.fit_transform(y)

# # Feature engineering
# def create_interaction_features(X):
#     numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
#     for i in range(len(numeric_cols)):
#         for j in range(i+1, len(numeric_cols)):
#             col1, col2 = numeric_cols[i], numeric_cols[j]
#             X[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-6)
#             X[f'{col1}_{col2}_product'] = X[col1] * X[col2]
#     return X

# X = create_interaction_features(X)

# # Handle categorical data
# categorical_cols = X.select_dtypes(include=['object']).columns
# X = pd.get_dummies(X, columns=categorical_cols)

# # Feature selection
# selector = SelectKBest(score_func=f_classif, k='all')
# X_selected = selector.fit_transform(X, y_encoded)
# selected_features_mask = selector.get_support()
# selected_feature_names = X.columns[selected_features_mask].tolist()
# X = X[selected_feature_names]

# # Advanced preprocessing
# def preprocess_features(X):
#     X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    
#     power_transformer = PowerTransformer(method='yeo-johnson')
#     robust_scaler = RobustScaler()
    
#     X_power = power_transformer.fit_transform(X)
#     X_robust = robust_scaler.fit_transform(X_power)
    
#     return X_robust

# X = preprocess_features(X)

# # Resampling with SMOTEENN
# smote_enn = SMOTEENN(random_state=42)
# X_resampled, y_resampled = smote_enn.fit_resample(X, y_encoded)

# # Re-encode labels after resampling
# label_encoder_resampled = LabelEncoder()
# y_resampled = label_encoder_resampled.fit_transform(y_resampled)
# num_classes = len(np.unique(y_resampled))

# # Validate class distribution
# print("Final class distribution:", {label: count for label, count in zip(*np.unique(y_resampled, return_counts=True))})

# # Define input shape
# input_shape = (X_resampled.shape[1],)

# # Ensuring a Minimum Number of Samples Per Class
# def check_min_samples(y, min_samples=5):
#     counts = np.bincount(y)
#     return np.all(counts >= min_samples)

# if not check_min_samples(y_resampled, min_samples=5):
#     print("Warning: Some classes have too few samples. Consider further resampling.")

# # Stratified K-Fold with Class Validation
# n_splits = 5
# kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# # Deep learning model
# def create_deep_model(input_shape, num_classes):
#     inputs = keras.Input(shape=input_shape)

#     x = Dense(512, kernel_regularizer=keras.regularizers.l2(0.01))(inputs)
#     x = LeakyReLU(0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.5)(x)

#     skip = x

#     x = Dense(256, kernel_regularizer=keras.regularizers.l2(0.01))(x)
#     x = LeakyReLU(0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.4)(x)

#     x = keras.layers.concatenate([x, skip])

#     x = Dense(128, kernel_regularizer=keras.regularizers.l2(0.01))(x)
#     x = LeakyReLU(0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.3)(x)

#     outputs = Dense(num_classes, activation='softmax')(x)

#     return keras.Model(inputs, outputs)

# # Training function with Class Handling
# def train_ensemble(X, y, input_shape, num_classes):
#     ensemble_predictions = []
#     fold_accuracies = []

#     for fold, (train_idx, val_idx) in enumerate(kf.split(X, y)):
#         print(f"\nFold {fold+1}/{n_splits}")

#         X_train, X_val = X[train_idx], X[val_idx]
#         y_train, y_val = y[train_idx], y[val_idx]

#         # Ensure all classes are present
#         train_classes = np.unique(y_train)
#         missing_classes = set(range(num_classes)) - set(train_classes)
        
#         if missing_classes:
#             print(f"⚠️ Warning: Fold {fold+1} is missing classes {missing_classes}. Applying SMOTE.")
#             smote = SMOTEENN(random_state=42)
#             X_train, y_train = smote.fit_resample(X_train, y_train)

#         # Create fresh models per fold
#         models = [
#             create_deep_model(input_shape, num_classes),
#             xgb.XGBClassifier(
#                 learning_rate=0.01,
#                 n_estimators=200,
#                 max_depth=7,
#                 objective='multi:softprob',
#                 num_class=num_classes,
#                 random_state=42+fold
#             )
#         ]

#         # Train models
#         fold_preds = []
#         for model in models:
#             if isinstance(model, keras.Model):
#                 model.compile(
#                     optimizer=keras.optimizers.Adam(0.001),
#                     loss='sparse_categorical_crossentropy',
#                     metrics=['accuracy']
#                 )
#                 model.fit(
#                     X_train, y_train,
#                     validation_data=(X_val, y_val),
#                     epochs=100,
#                     batch_size=32,
#                     callbacks=[EarlyStopping(patience=20, restore_best_weights=True)],
#                     verbose=0
#                 )
#                 pred = model.predict(X_val)
#             else:
#                 model.fit(X_train, y_train)
#                 pred = model.predict_proba(X_val)

#             fold_preds.append(pred)

#         # Ensemble predictions
#         avg_pred = np.mean(fold_preds, axis=0)
#         fold_acc = accuracy_score(y_val, np.argmax(avg_pred, axis=1))
#         print(f"Fold {fold+1} Accuracy: {fold_acc:.4f}")
#         fold_accuracies.append(fold_acc)

#         ensemble_predictions.append((val_idx, avg_pred))

#     return ensemble_predictions, np.mean(fold_accuracies)

# # Execute training
# ensemble_preds, mean_acc = train_ensemble(X_resampled, y_resampled, input_shape, num_classes)

# # Save best model
# best_model = create_deep_model(input_shape, num_classes)
# best_model.compile(
#     optimizer=keras.optimizers.Adam(0.001),
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# best_model.fit(X_resampled, y_resampled, epochs=100, batch_size=32, callbacks=[EarlyStopping(patience=20)], validation_split=0.2, verbose=0)
# best_model.save('crop_model.keras')







# from sklearn.preprocessing import PowerTransformer, RobustScaler
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
# from tensorflow.keras.callbacks import EarlyStopping
# from sklearn.model_selection import StratifiedKFold
# from sklearn.preprocessing import LabelEncoder
# from sklearn.feature_selection import SelectKBest, f_classif
# from imblearn.combine import SMOTEENN
# import xgboost as xgb
# from sklearn.metrics import accuracy_score
# import matplotlib.pyplot as plt
# import os

# # Create directories for saving preprocessing files and graphs
# os.makedirs('preprocessing', exist_ok=True)
# os.makedirs('graphs', exist_ok=True)

# # Load data
# data = pd.read_csv('crop_dataset_fixed.csv')
# target_column = 'Crop'

# # Separate features and labels
# X = data.drop(columns=[target_column])
# y = data[target_column]

# # Label encoding
# label_encoder = LabelEncoder()
# y_encoded = label_encoder.fit_transform(y)

# # Feature engineering
# def create_interaction_features(X):
#     numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
#     for i in range(len(numeric_cols)):
#         for j in range(i+1, len(numeric_cols)):
#             col1, col2 = numeric_cols[i], numeric_cols[j]
#             X[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-6)
#             X[f'{col1}_{col2}_product'] = X[col1] * X[col2]
#     return X

# X = create_interaction_features(X)

# # Handle categorical data
# categorical_cols = X.select_dtypes(include=['object']).columns
# X = pd.get_dummies(X, columns=categorical_cols)

# # Feature selection
# selector = SelectKBest(score_func=f_classif, k='all')
# X_selected = selector.fit_transform(X, y_encoded)
# selected_features_mask = selector.get_support()
# selected_feature_names = X.columns[selected_features_mask].tolist()
# X = X[selected_feature_names]

# # Save feature selection and label encoding
# np.save('preprocessing/selected_feature_names.npy', selected_feature_names)
# np.save('preprocessing/selected_features_mask.npy', selected_features_mask)
# np.save('preprocessing/label_classes.npy', label_encoder.classes_)

# # Advanced preprocessing
# def preprocess_features(X):
#     X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    
#     power_transformer = PowerTransformer(method='yeo-johnson')
#     robust_scaler = RobustScaler()
    
#     X_power = power_transformer.fit_transform(X)
#     X_robust = robust_scaler.fit_transform(X_power)
    
#     return X_robust, power_transformer, robust_scaler

# X, power_transformer, robust_scaler = preprocess_features(X)

# # Save transformers
# np.save('preprocessing/power_transformer.npy', power_transformer)
# np.save('preprocessing/robust_scaler.npy', robust_scaler)

# # Resampling with SMOTEENN
# smote_enn = SMOTEENN(random_state=42)
# X_resampled, y_resampled = smote_enn.fit_resample(X, y_encoded)

# # Re-encode labels after resampling
# label_encoder_resampled = LabelEncoder()
# y_resampled = label_encoder_resampled.fit_transform(y_resampled)
# num_classes = len(np.unique(y_resampled))

# # Define input shape
# input_shape = (X_resampled.shape[1],)

# # Deep learning model
# def create_deep_model(input_shape, num_classes):
#     inputs = keras.Input(shape=input_shape)

#     x = Dense(512, kernel_regularizer=keras.regularizers.l2(0.01))(inputs)
#     x = LeakyReLU(0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.5)(x)

#     skip = x

#     x = Dense(256, kernel_regularizer=keras.regularizers.l2(0.01))(x)
#     x = LeakyReLU(0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.4)(x)

#     x = keras.layers.concatenate([x, skip])

#     x = Dense(128, kernel_regularizer=keras.regularizers.l2(0.01))(x)
#     x = LeakyReLU(0.1)(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.3)(x)

#     outputs = Dense(num_classes, activation='softmax')(x)

#     return keras.Model(inputs, outputs)

# # Training function with Class Handling
# def train_ensemble(X, y, input_shape, num_classes, n_splits=5):
#     ensemble_predictions = []
#     fold_accuracies = []
#     histories = []  # To store the training history for each fold

#     # Stratified K-Fold initialization
#     kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

#     for fold, (train_idx, val_idx) in enumerate(kf.split(X, y)):
#         print(f"\nFold {fold+1}/{n_splits}")

#         X_train, X_val = X[train_idx], X[val_idx]
#         y_train, y_val = y[train_idx], y[val_idx]

#         # Ensure all classes are present
#         train_classes = np.unique(y_train)
#         missing_classes = set(range(num_classes)) - set(train_classes)
        
#         if missing_classes:
#             print(f"⚠️ Warning: Fold {fold+1} is missing classes {missing_classes}. Applying SMOTE.")
#             smote = SMOTEENN(random_state=42)
#             X_train, y_train = smote.fit_resample(X_train, y_train)

#         # Create fresh models per fold
#         models = [
#             create_deep_model(input_shape, num_classes),
#             xgb.XGBClassifier(
#                 learning_rate=0.01,
#                 n_estimators=200,
#                 max_depth=7,
#                 objective='multi:softprob',
#                 num_class=num_classes,
#                 random_state=42+fold
#             )
#         ]

#         # Train models
#         fold_preds = []
#         for model in models:
#             if isinstance(model, keras.Model):
#                 model.compile(
#                     optimizer=keras.optimizers.Adam(0.001),
#                     loss='sparse_categorical_crossentropy',
#                     metrics=['accuracy']
#                 )
#                 history = model.fit(
#                     X_train, y_train,
#                     validation_data=(X_val, y_val),
#                     epochs=100,
#                     batch_size=32,
#                     callbacks=[EarlyStopping(patience=20, restore_best_weights=True)],
#                     verbose=0
#                 )
#                 fold_acc = history.history['val_accuracy'][-1]  # Get the last validation accuracy
#                 histories.append(history)  # Store the history for later use
#                 pred = model.predict(X_val)
#             else:
#                 model.fit(X_train, y_train)
#                 pred = model.predict_proba(X_val)

#             fold_preds.append(pred)

#         # Ensemble predictions
#         avg_pred = np.mean(fold_preds, axis=0)
#         fold_acc = accuracy_score(y_val, np.argmax(avg_pred, axis=1))
#         print(f"Fold {fold+1} Accuracy: {fold_acc:.4f}")
#         fold_accuracies.append(fold_acc)

#         ensemble_predictions.append((val_idx, avg_pred))

#     # Return the predictions, average accuracy, and the list of histories
#     return ensemble_predictions, np.mean(fold_accuracies), histories

# # Execute training
# ensemble_preds, mean_acc, histories = train_ensemble(X_resampled, y_resampled, input_shape, num_classes)

# # Save best model
# best_model = create_deep_model(input_shape, num_classes)
# best_model.compile(
#     optimizer=keras.optimizers.Adam(0.001),
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# best_model.fit(X_resampled, y_resampled, epochs=100, batch_size=32, callbacks=[EarlyStopping(patience=20)], validation_split=0.2, verbose=0)
# best_model.save('crop_model.keras')

# # Save training history plots for each fold
# for fold_number, history in enumerate(histories, 1):
#     plt.figure(figsize=(10, 6))
#     plt.plot(history.history['accuracy'], label='Training Accuracy')
#     plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
#     plt.xlabel('Epochs')
#     plt.ylabel('Accuracy')
#     plt.title(f'Fold {fold_number} Accuracy')
#     plt.legend()
#     plt.savefig(f'graphs/fold_{fold_number}_accuracy.png')
#     plt.close()

#     # Plot Loss for each fold
#     plt.figure(figsize=(10, 6))
#     plt.plot(history.history['loss'], label='Training Loss')
#     plt.plot(history.history['val_loss'], label='Validation Loss')
#     plt.xlabel('Epochs')
#     plt.ylabel('Loss')
#     plt.title(f'Fold {fold_number} Loss')
#     plt.legend()
#     plt.savefig(f'graphs/fold_{fold_number}_loss.png')
#     plt.close()




import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder, PowerTransformer, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import SMOTE, RandomOverSampler
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import os
import joblib

# Create directories
os.makedirs('preprocessing', exist_ok=True)
os.makedirs('graphs', exist_ok=True)

# Load dataset
data = pd.read_csv('crop_dataset.csv')
target_column = 'Crop'

# Print initial class distribution
print("Initial class distribution:")
class_dist = data[target_column].value_counts()
print(class_dist)
print(f"Total samples: {len(data)}, Total classes: {len(class_dist)}")

# Increase minimum samples required to ensure better stratification
min_samples_required = 20  # Increased from 10 to 20 to ensure better distribution
class_counts = data[target_column].value_counts()
valid_classes = class_counts[class_counts >= min_samples_required].index
excluded_classes = class_counts[class_counts < min_samples_required]

if not excluded_classes.empty:
    print(f"\n⚠️ Excluding crops with < {min_samples_required} samples:\n{excluded_classes}")
    print(f"Number of excluded classes: {len(excluded_classes)}")

data = data[data[target_column].isin(valid_classes)].copy()
print(f"\nRemaining samples: {len(data)}, Remaining classes: {len(valid_classes)}")

# If we have very few classes left, consider relaxing the criteria
if len(valid_classes) < 5 and not excluded_classes.empty:
    print("\n⚠️ Too few classes remain. Relaxing criteria to include more classes.")
    min_samples_required = 10  # Relaxed criteria
    valid_classes = class_counts[class_counts >= min_samples_required].index
    data = pd.read_csv('crop_dataset.csv')  # Reload original data
    data = data[data[target_column].isin(valid_classes)].copy()
    print(f"After relaxing criteria: {len(data)} samples, {len(valid_classes)} classes")

# Encode labels
label_encoder = LabelEncoder()
data[target_column] = label_encoder.fit_transform(data[target_column])
np.save('preprocessing/label_classes.npy', label_encoder.classes_)

# Split features and encoded labels
X = data.drop(columns=[target_column])
y_encoded = data[target_column].values  # Convert to numpy array

# Check encoded class distribution
print("\nEncoded class distribution:")
encoded_dist = pd.Series(y_encoded).value_counts().sort_index()
print(encoded_dist)

# Feature engineering
def create_interaction_features(X):
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
    # Print columns being used for interaction features
    print(f"\nCreating interaction features from: {numeric_cols.tolist()}")
    
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            X[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-6)
            X[f'{col1}_{col2}_product'] = X[col1] * X[col2]
    return X

X = create_interaction_features(X)
print(f"Features after interaction: {X.shape[1]}")

# Handle any unexpected categorical features
X = pd.get_dummies(X)
print(f"Features after one-hot encoding: {X.shape[1]}")

# Feature selection
selector = SelectKBest(score_func=f_classif, k='all')
X_selected = selector.fit_transform(X, y_encoded)
selected_features_mask = selector.get_support()
selected_feature_names = X.columns[selected_features_mask].tolist()

# Display top features with scores
feature_scores = selector.scores_
sorted_idx = np.argsort(feature_scores)[::-1]
top_features = [(X.columns[i], feature_scores[i]) for i in sorted_idx[:10]]
print("\nTop 10 features by importance:")
for feature, score in top_features:
    print(f"{feature}: {score:.2f}")

# Keep all features or select top k
k_features = min(30, X.shape[1])  # Limit to top 30 features
selector = SelectKBest(score_func=f_classif, k=k_features)
X_selected = selector.fit_transform(X, y_encoded)
selected_features_mask = selector.get_support()
selected_feature_names = X.columns[selected_features_mask].tolist()

print(f"\nSelected {len(selected_feature_names)} features for model training")
X = X[selected_feature_names]

# Save selected feature info
np.save('preprocessing/selected_feature_names.npy', np.array(selected_feature_names, dtype=object))
np.save('preprocessing/selected_features_mask.npy', selected_features_mask)

# Preprocessing (transform, scale)
def preprocess_features(X):
    # Check for and handle any NaN or inf values
    X = X.replace([np.inf, -np.inf], np.nan)
    
    if X.isna().any().any():
        print(f"Found {X.isna().sum().sum()} NaN values, filling with 0")
        X = X.fillna(0)
    
    power_transformer = PowerTransformer(method='yeo-johnson')
    robust_scaler = RobustScaler()
    
    # Convert to numpy array if it's a DataFrame
    if isinstance(X, pd.DataFrame):
        X_values = X.values
    else:
        X_values = X
    
    X_power = power_transformer.fit_transform(X_values)
    X_robust = robust_scaler.fit_transform(X_power)
    return X_robust, power_transformer, robust_scaler

X_processed, power_transformer, robust_scaler = preprocess_features(X)

# Save preprocessing objects
joblib.dump(power_transformer, 'preprocessing/power_transformer.joblib')
joblib.dump(robust_scaler, 'preprocessing/robust_scaler.joblib')

# Get class distribution after preprocessing to check for any issues
print("\nClass distribution after preprocessing:")
print(pd.Series(y_encoded).value_counts().sort_index())

# # Determine appropriate resampling strategy based on class distribution
# # Given the initial dataset is balanced, resampling might not be necessary or could be detrimental.
# # If feature engineering/selection creates imbalance, consider SMOTE.
# min_class_count_before_resample = pd.Series(y_encoded).value_counts().min()
# num_classes_before_resample = len(np.unique(y_encoded))

# # For now, let's proceed without resampling as the initial dataset is balanced.
# # If you observe imbalance after feature processing that harms performance,
# # you can re-enable a resampling strategy here.
print("\nSkipping resampling as initial dataset is balanced.")
X_resampled = X_processed
y_resampled = y_encoded

# print(f"Data shape after resampling: {X_resampled.shape}")
# print("Class distribution after resampling:")
# resampled_dist = pd.Series(y_resampled).value_counts().sort_index()
# print(resampled_dist)


# Determine num_classes and input_shape AFTER potential resampling and BEFORE splitting
# This was a key source of the error.
num_classes = len(np.unique(y_resampled)) # Number of unique classes in the data to be split
input_shape = (X_resampled.shape[1],)
print(f"\nNumber of unique classes for model: {num_classes}")
print(f"Input shape for model: {input_shape}")

# Deep Learning Model - Simplified for small datasets
def create_deep_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    x = Dense(128, kernel_regularizer=keras.regularizers.l2(0.01))(inputs)
    x = LeakyReLU(0.1)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)

    x = Dense(64, kernel_regularizer=keras.regularizers.l2(0.01))(x)
    x = LeakyReLU(0.1)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)

    outputs = Dense(num_classes, activation='softmax')(x)
    return keras.Model(inputs, outputs)

# ALTERNATIVE APPROACH: Single train/test split instead of cross-validation
# This avoids the issues with rare classes in folds
print("\nUsing single train/test split.") # Removed "due to imbalanced classes" as we are not heavily resampling for now

# Check for classes that have too few samples for stratification
class_counts = pd.Series(y_resampled).value_counts()
min_class_count = class_counts.min()

# If any class has too few samples, don't use stratification
if min_class_count < 2: # Stratification requires at least 2 samples per class for binary, or n_splits for k-fold
    print(f"⚠️ At least one class has only {min_class_count} sample(s), which is too few for stratification.")
    print("Disabling stratification for train/test split.")
    stratify_param = None
else:
    stratify_param = y_resampled

# Split into train/test (80/20)
X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(
    X_resampled, y_resampled, 
    test_size=0.2, 
    random_state=42,
    stratify=stratify_param  # Only stratify if we have enough samples per class
)
# Make copies to avoid modifying original split data if further adjustments are needed
X_train, X_test, y_train, y_test = X_train_orig.copy(), X_test_orig.copy(), y_train_orig.copy(), y_test_orig.copy()

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Ensure all classes present in y_resampled are represented in y_train for model fitting
# This is crucial if num_classes was based on y_resampled.
# A simpler way is to ensure num_classes for the model is based on y_train.

final_num_classes_for_model = len(np.unique(np.concatenate((y_train, y_test)))) # Safest way to get num_classes
print(f"Final number of classes the model will be trained for: {final_num_classes_for_model}")

# The adjustment logic for missing classes was complex and likely a source of error.
# If stratification is disabled, it's possible for train or test to miss classes.
# A robust way is to ensure the model's output layer matches the total unique classes
# found in the *entire* dataset it's supposed to learn from (y_resampled).
# However, the error `Received a label value of 25 which is outside the valid range of [0, 25)`
# means the model was defined for `num_classes = 25` (labels 0-24), but a label `25` appeared.
# This implies `num_classes` was miscalculated.

# Let's redefine num_classes based on the actual data the model will see.
# The labels should be 0 to N-1 where N is the number of unique classes.
# If LabelEncoder was fit on the original `y`, its `classes_` attribute holds all original classes.
# `y_encoded` (and thus `y_resampled` if no new classes were made by SMOTE) should have labels from 0 to len(label_encoder.classes_)-1.

# The most robust `num_classes` is `len(label_encoder.classes_)` if `y_encoded` was derived from it.
# Or, if `y_resampled` could have different classes, then `len(np.unique(y_resampled))`.
# The error indicates `num_classes` was likely `len(np.unique(y_train))` which might be less than `len(np.unique(y_resampled))`.

# Let's use the number of classes from the original encoding, as SMOTE(ENN) should not create new classes.
num_classes = len(label_encoder.classes_) # This should be the true number of classes
print(f"Re-confirmed number of classes based on original LabelEncoder: {num_classes}")

if np.max(y_train) >= num_classes or np.max(y_test) >= num_classes:
    print("ERROR: Max label in y_train or y_test is out of bounds for num_classes!")
    # This would indicate a serious issue in label generation or splitting.

# Train neural network model
print("\nTraining neural network model...")
nn_model = create_deep_model(input_shape, num_classes)
nn_model.compile(
    optimizer=keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

nn_history = nn_model.fit(
    X_train, y_train, # Use the potentially adjusted y_train
    validation_data=(X_test, y_test),
    epochs=50,
    batch_size=32,
    callbacks=[early_stopping],
    verbose=1
)

# Train XGBoost model
print("\nTraining XGBoost model...")
xgb_model = xgb.XGBClassifier(
    learning_rate=0.01,
    n_estimators=100, # Reduced for faster iteration, can be tuned
    max_depth=4,
    objective='multi:softprob',
    num_class=num_classes,
    random_state=42
)

try:
    xgb_model.fit(X_train, y_train) # Use the potentially adjusted y_train
    print("XGBoost model training completed")
except Exception as e:
    print(f"XGBoost training failed: {e}")
    xgb_model = None

# Evaluate neural network
nn_preds = nn_model.predict(X_test)
nn_pred_classes = np.argmax(nn_preds, axis=1)
nn_accuracy = accuracy_score(y_test, nn_pred_classes)
print(f"\nNeural Network Test Accuracy: {nn_accuracy:.4f}")

# Try to get detailed metrics
try:
    nn_report = classification_report(y_test, nn_pred_classes, output_dict=True)
    print("Neural Network Classification Report:")
    print(f"Weighted Precision: {nn_report['weighted avg']['precision']:.4f}")
    print(f"Weighted Recall: {nn_report['weighted avg']['recall']:.4f}")
    print(f"Weighted F1-score: {nn_report['weighted avg']['f1-score']:.4f}")
except Exception as e:
    print(f"Could not generate detailed metrics: {e}")

# Evaluate XGBoost if training succeeded
if xgb_model is not None:
    xgb_preds = xgb_model.predict(X_test)
    xgb_accuracy = accuracy_score(y_test, xgb_preds)
    print(f"XGBoost Test Accuracy: {xgb_accuracy:.4f}")
    
    # Try to get detailed metrics
    try:
        xgb_report = classification_report(y_test, xgb_preds, output_dict=True)
        print("XGBoost Classification Report:")
        print(f"Weighted Precision: {xgb_report['weighted avg']['precision']:.4f}")
        print(f"Weighted Recall: {xgb_report['weighted avg']['recall']:.4f}")
        print(f"Weighted F1-score: {xgb_report['weighted avg']['f1-score']:.4f}")
    except Exception as e:
        print(f"Could not generate detailed metrics: {e}")

# Create ensemble if both models are available
if xgb_model is not None:
    print("\nCreating ensemble model...")
    # Simple averaging ensemble
    xgb_proba = xgb_model.predict_proba(X_test)
    ensemble_proba = (nn_preds + xgb_proba) / 2
    ensemble_preds = np.argmax(ensemble_proba, axis=1)
    ensemble_accuracy = accuracy_score(y_test, ensemble_preds)
    print(f"Ensemble Test Accuracy: {ensemble_accuracy:.4f}")
    
    # Determine best model
    if ensemble_accuracy > max(nn_accuracy, xgb_accuracy):
        print("Ensemble model is best")
        best_model_type = "ensemble"
    elif nn_accuracy > xgb_accuracy:
        print("Neural Network model is best")
        best_model_type = "nn"
    else:
        print("XGBoost model is best")
        best_model_type = "xgb"
else:
    print("Using Neural Network as the final model (XGBoost failed)")
    best_model_type = "nn"

# Save neural network model
nn_model.save('crop_nn_model.keras')
print("✅ Neural Network model saved as 'crop_nn_model.keras'")

# Save XGBoost model if available
if xgb_model is not None:
    joblib.dump(xgb_model, 'crop_xgb_model.joblib')
    print("✅ XGBoost model saved as 'crop_xgb_model.joblib'")

# Also save a "best" model reference
with open('best_model.txt', 'w') as f:
    f.write(best_model_type)
print(f"✅ Best model type ({best_model_type}) saved to 'best_model.txt'")

# Save model architecture as a JSON file for easier inspection
with open('model_architecture.json', 'w') as f:
    f.write(nn_model.to_json())

# Save training plots for neural network
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(nn_history.history['accuracy'], label='Training Accuracy')
plt.plot(nn_history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(nn_history.history['loss'], label='Training Loss')
plt.plot(nn_history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig('graphs/model_performance.png')
plt.close()

# Save confusion matrix if possible
try:
    from sklearn.metrics import confusion_matrix
    import seaborn as sns
    
    # Create confusion matrix
    cm = confusion_matrix(y_test, nn_pred_classes)
    
    # If there are many classes, limit the visualization
    if len(np.unique(y_test)) > 20:
        print("Too many classes for confusion matrix visualization")
    else:
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('graphs/confusion_matrix.png')
        plt.close()
        print("✅ Confusion matrix saved to 'graphs/confusion_matrix.png'")
except Exception as e:
    print(f"Could not generate confusion matrix: {e}")

# # Create a prediction function
# def predict_crop(features_dict):
#     """
#     Make a prediction for crop recommendation based on soil and weather features.
    
#     Args:
#         features_dict: Dictionary with keys for N, P, K, Temp, Humidity, pH, Soil Moisture
        
#     Returns:
#         Predicted crop name and probability
#     """
#     # Convert input to DataFrame
#     input_df = pd.DataFrame([features_dict])
    
#     # Create interaction features
#     for i, col1 in enumerate(['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)']):
#         for j, col2 in enumerate(['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)'])[i+1:]:
#             if col1 in input_df.columns and col2 in input_df.columns:
#                 input_df[f'{col1}_{col2}_ratio'] = input_df[col1] / (input_df[col2] + 1e-6)
#                 input_df[f'{col1}_{col2}_product'] = input_df[col1] * input_df[col2]
    
#     # One-hot encode any categorical features (if any)
#     input_df = pd.get_dummies(input_df)
    
#     # Ensure all selected features are present
#     for feature in selected_feature_names:
#         if feature not in input_df.columns:
#             input_df[feature] = 0
    
#     # Select only the features used in training
#     input_df = input_df[selected_feature_names]
    
#     # Apply transformations
#     input_transformed = power_transformer.transform(input_df)
#     input_scaled = robust_scaler.transform(input_transformed)
    
#     # Get predictions
#     if best_model_type == "nn":
#         probabilities = nn_model.predict(input_scaled)[0]
#         predicted_class_idx = np.argmax(probabilities)
#         confidence = probabilities[predicted_class_idx]
#     elif best_model_type == "xgb":
#         probabilities = xgb_model.predict_proba(input_scaled)[0]
#         predicted_class_idx = np.argmax(probabilities)
#         confidence = probabilities[predicted_class_idx]
#     else:  # ensemble
#         nn_probs = nn_model.predict(input_scaled)[0]
#         xgb_probs = xgb_model.predict_proba(input_scaled)[0]
#         probabilities = (nn_probs + xgb_probs) / 2
#         predicted_class_idx = np.argmax(probabilities)
#         confidence = probabilities[predicted_class_idx]
    
#     # Convert back to original crop name
#     predicted_crop = label_encoder.classes_[predicted_class_idx]
    
#     return {
#         'crop': predicted_crop,
#         'confidence': float(confidence),
#         'class_idx': int(predicted_class_idx)
#     }

# # Save the prediction function
# with open('prediction_function.py', 'w') as f:
#     f.write("""
# import pandas as pd
# import numpy as np
# import joblib
# import os
# import tensorflow as tf
# from tensorflow import keras

# # Load preprocessing objects
# power_transformer = joblib.load('preprocessing/power_transformer.joblib')
# robust_scaler = joblib.load('preprocessing/robust_scaler.joblib')
# selected_feature_names = np.load('preprocessing/selected_feature_names.npy', allow_pickle=True)
# label_classes = np.load('preprocessing/label_classes.npy')

# # Load models
# nn_model = keras.models.load_model('crop_nn_model.keras')
# try:
#     xgb_model = joblib.load('crop_xgb_model.joblib')
#     have_xgb = True
# except:
#     have_xgb = False

# # Read best model type
# with open('best_model.txt', 'r') as f:
#     best_model_type = f.read().strip()

# def predict_crop(features_dict):
#     \"\"\"
#     Make a prediction for crop recommendation based on soil and weather features.
    
#     Args:
#         features_dict: Dictionary with keys for N, P, K, Temp, Humidity, pH, Soil Moisture
        
#     Returns:
#         Predicted crop name and probability
#     \"\"\"
#     # Convert input to DataFrame
#     input_df = pd.DataFrame([features_dict])
    
#     # Create interaction features
#     for i, col1 in enumerate(['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)']):
#         for j, col2 in enumerate(['N (ppm)', 'P (ppm)', 'K (ppm)', 'Temp (°C)', 'Humidity (%)', 'pH', 'Soil Moisture (%)'])[i+1:]:
#             if col1 in input_df.columns and col2 in input_df.columns:
#                 input_df[f'{col1}_{col2}_ratio'] = input_df[col1] / (input_df[col2] + 1e-6)
#                 input_df[f'{col1}_{col2}_product'] = input_df[col1] * input_df[col2]
    
#     # One-hot encode any categorical features (if any)
#     input_df = pd.get_dummies(input_df)
    
#     # Ensure all selected features are present
#     for feature in selected_feature_names:
#         if feature not in input_df.columns:
#             input_df[feature] = 0
    
#     # Select only the features used in training
#     input_df = input_df[selected_feature_names]
    
#     # Apply transformations
#     input_transformed = power_transformer.transform(input_df)
#     input_scaled = robust_scaler.transform(input_transformed)
    
#     # Get predictions
#     if best_model_type == "nn" or not have_xgb:
#         probabilities = nn_model.predict(input_scaled)[0]
#         predicted_class_idx = np.argmax(probabilities)
#         confidence = probabilities[predicted_class_idx]
#     elif best_model_type == "xgb":
#         probabilities = xgb_model.predict_proba(input_scaled)[0]
#         predicted_class_idx = np.argmax(probabilities)
#         confidence = probabilities[predicted_class_idx]
#     else:  # ensemble
#         nn_probs = nn_model.predict(input_scaled)[0]
#         xgb_probs = xgb_model.predict_proba(input_scaled)[0]
#         probabilities = (nn_probs + xgb_probs) / 2
#         predicted_class_idx = np.argmax(probabilities)
#         confidence = probabilities[predicted_class_idx]
    
#     # Convert back to original crop name
#     predicted_crop = label_classes[predicted_class_idx]
    
#     return {
#         'crop': predicted_crop,
#         'confidence': float(confidence),
#         'class_idx': int(predicted_class_idx)
#     }
# """)

# print("\n✅ Prediction function saved to 'prediction_function.py'")

# Save a summary of the model and training process
# Save a summary of the model and training process
with open('training_summary.txt', 'w', encoding='utf-8') as f:
    f.write(f"Crop Classification Model Training Summary\n")
    f.write(f"========================================\n\n")
    f.write(f"Dataset Information:\n")
    f.write(f"- Total classes: {num_classes}\n")
    f.write(f"- Total samples after filtering: {len(data)}\n")
    f.write(f"- Samples after resampling: {len(y_resampled)}\n\n")
    
    f.write(f"Model Architecture:\n")
    # Instead of using summary with print_fn, capture the summary as string
    # and write it safely
    try:
        # Using StringIO to capture the summary output
        import io
        from contextlib import redirect_stdout
        
        summary_str = io.StringIO()
        with redirect_stdout(summary_str):
            nn_model.summary()
        
        f.write(summary_str.getvalue())
    except Exception as e:
        f.write(f"Could not write full model summary: {str(e)}\n")
        f.write(f"- Input shape: {input_shape}\n")
        f.write(f"- Output classes: {num_classes}\n")
        f.write(f"- Model type: Sequential with Dense layers\n")
    
    f.write(f"\nTraining Performance:\n")
    if nn_history:
        f.write(f"- Neural network test accuracy: {nn_accuracy:.4f}\n")
        f.write(f"- Best validation accuracy: {max(nn_history.history['val_accuracy']):.4f}\n")
        f.write(f"- Best validation loss: {min(nn_history.history['val_loss']):.4f}\n")
    
    if xgb_model is not None:
        f.write(f"- XGBoost test accuracy: {xgb_accuracy:.4f}\n")
    
    if xgb_model is not None:
        f.write(f"- Ensemble test accuracy: {ensemble_accuracy:.4f}\n")
    
    f.write(f"\nSelected Features ({len(selected_feature_names)}):\n")
    for i, feature in enumerate(selected_feature_names, 1):
        f.write(f"{i}. {feature}\n")

print("\n✅ Training summary saved to 'training_summary.txt'")
print("\n✅ Training completed successfully!")

# Print recommendations for deployment
print("\n=== RECOMMENDATIONS FOR DEPLOYMENT ===")
print("1. Use the saved models in 'crop_nn_model.keras' and/or 'crop_xgb_model.joblib'")
print("2. Use the prediction function in 'prediction_function.py' for making new predictions")
print("3. Ensure all preprocessing objects in the 'preprocessing' directory are available")
print("4. Consider collecting more data for classes with few samples")
print("5. Periodically retrain the model as more data becomes available")