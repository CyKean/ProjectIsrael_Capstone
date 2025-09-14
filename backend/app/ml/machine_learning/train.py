# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
# from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
# from sklearn.preprocessing import StandardScaler, LabelEncoder, PowerTransformer, RobustScaler
# from sklearn.ensemble import VotingClassifier
# from sklearn.feature_selection import SelectKBest, f_classif
# from imblearn.over_sampling import SMOTE
# from imblearn.combine import SMOTEENN
# import xgboost as xgb
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.metrics import ConfusionMatrixDisplay
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.subplots import make_subplots

# # Load data
# data = pd.read_csv('crop_dataset.csv')
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

# # Enhanced sampling - Use SMOTE instead of SMOTEENN to preserve all classes
# smote = SMOTE(random_state=42)
# X_resampled, y_resampled = smote.fit_resample(X, y)

# # Label encoding - Do this AFTER resampling to ensure consistent classes
# label_encoder = LabelEncoder()
# y_encoded = label_encoder.fit_transform(y_resampled)

# # Get the actual number of classes after resampling
# num_classes = len(np.unique(y_encoded))
# print(f"Number of classes after resampling: {num_classes}")
# print(f"Class labels: {np.unique(y_encoded)}")

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
        
#         # XGBoost model - FIXED: Use correct number of classes
#         xgb_model = xgb.XGBClassifier(
#             learning_rate=0.01,
#             n_estimators=200,
#             max_depth=7,
#             min_child_weight=1,
#             gamma=0.1,
#             subsample=0.8,
#             colsample_bytree=0.8,
#             objective='multi:softprob',
#             num_class=num_classes,  # Use actual number of classes
#             random_state=42+i
#         )
#         models.append(xgb_model)
    
#     return models

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

# # Function to generate training graphs
# def generate_training_graphs(history, fold_num=None, model_type="Deep Learning"):
#     """
#     Generate comprehensive training graphs for model performance
#     """
#     if fold_num:
#         title_suffix = f" - Fold {fold_num}"
#     else:
#         title_suffix = ""
    
#     # Create subplots
#     fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
#     fig.suptitle(f'{model_type} Training Performance{title_suffix}', fontsize=16, fontweight='bold')
    
#     # Plot training & validation accuracy
#     ax1.plot(history.history['accuracy'], label='Training Accuracy', color='blue', linewidth=2)
#     ax1.plot(history.history['val_accuracy'], label='Validation Accuracy', color='red', linewidth=2)
#     ax1.set_title('Model Accuracy')
#     ax1.set_xlabel('Epoch')
#     ax1.set_ylabel('Accuracy')
#     ax1.legend()
#     ax1.grid(True, alpha=0.3)
    
#     # Plot training & validation loss
#     ax2.plot(history.history['loss'], label='Training Loss', color='blue', linewidth=2)
#     ax2.plot(history.history['val_loss'], label='Validation Loss', color='red', linewidth=2)
#     ax2.set_title('Model Loss')
#     ax2.set_xlabel('Epoch')
#     ax2.set_ylabel('Loss')
#     ax2.legend()
#     ax2.grid(True, alpha=0.3)
    
#     # Plot learning rate
#     if 'lr' in history.history:
#         ax3.plot(history.history['lr'], label='Learning Rate', color='green', linewidth=2)
#         ax3.set_title('Learning Rate Schedule')
#         ax3.set_xlabel('Epoch')
#         ax3.set_ylabel('Learning Rate')
#         ax3.set_yscale('log')
#         ax3.legend()
#         ax3.grid(True, alpha=0.3)
    
#     # Plot accuracy difference
#     train_acc = history.history['accuracy']
#     val_acc = history.history['val_accuracy']
#     acc_diff = [train_acc[i] - val_acc[i] for i in range(len(train_acc))]
#     ax4.plot(acc_diff, label='Train-Val Accuracy Difference', color='purple', linewidth=2)
#     ax4.axhline(y=0, color='black', linestyle='--', alpha=0.7)
#     ax4.set_title('Training vs Validation Accuracy Difference')
#     ax4.set_xlabel('Epoch')
#     ax4.set_ylabel('Accuracy Difference')
#     ax4.legend()
#     ax4.grid(True, alpha=0.3)
    
#     plt.tight_layout()
#     plt.savefig(f'training_performance{title_suffix.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
#     plt.close()

# # Function to generate evaluation graphs
# def generate_evaluation_graphs(y_true, y_pred, class_names, fold_accuracies=None):
#     """
#     Generate evaluation graphs including confusion matrix and accuracy plots
#     """
#     # Create confusion matrix
#     cm = confusion_matrix(y_true, y_pred)
    
#     # Plot confusion matrix
#     plt.figure(figsize=(12, 10))
#     sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
#                 xticklabels=class_names, yticklabels=class_names)
#     plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
#     plt.xlabel('Predicted Label')
#     plt.ylabel('True Label')
#     plt.xticks(rotation=45, ha='right')
#     plt.yticks(rotation=0)
#     plt.tight_layout()
#     plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
#     plt.close()
    
#     # Plot accuracy per class
#     class_accuracy = cm.diagonal() / cm.sum(axis=1)
#     plt.figure(figsize=(12, 6))
#     bars = plt.bar(range(len(class_names)), class_accuracy, color='skyblue', alpha=0.8)
#     plt.title('Accuracy per Class', fontsize=16, fontweight='bold')
#     plt.xlabel('Class')
#     plt.ylabel('Accuracy')
#     plt.xticks(range(len(class_names)), class_names, rotation=45, ha='right')
#     plt.ylim(0, 1)
    
#     # Add value labels on bars
#     for bar, acc in zip(bars, class_accuracy):
#         plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
#                 f'{acc:.3f}', ha='center', va='bottom')
    
#     plt.tight_layout()
#     plt.savefig('class_accuracy.png', dpi=300, bbox_inches='tight')
#     plt.close()
    
#     # Plot cross-validation fold accuracies if provided
#     if fold_accuracies is not None:
#         plt.figure(figsize=(10, 6))
#         folds = range(1, len(fold_accuracies) + 1)
#         plt.plot(folds, fold_accuracies, 'o-', color='green', linewidth=2, markersize=8)
#         plt.axhline(y=np.mean(fold_accuracies), color='red', linestyle='--', 
#                    label=f'Mean Accuracy: {np.mean(fold_accuracies):.4f}')
#         plt.title('Cross-Validation Fold Accuracies', fontsize=16, fontweight='bold')
#         plt.xlabel('Fold Number')
#         plt.ylabel('Accuracy')
#         plt.legend()
#         plt.grid(True, alpha=0.3)
#         plt.xticks(folds)
#         plt.ylim(0, 1)
        
#         # Add value labels on points
#         for i, acc in enumerate(fold_accuracies):
#             plt.text(folds[i], acc + 0.01, f'{acc:.4f}', ha='center', va='bottom')
        
#         plt.tight_layout()
#         plt.savefig('cv_accuracy.png', dpi=300, bbox_inches='tight')
#         plt.close()

# # Use StratifiedKFold instead of regular KFold to preserve class distribution
# n_splits = 5
# skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# # Train ensemble
# def train_ensemble(X, y, input_shape, num_classes):
#     ensemble_predictions = []
#     fold_accuracies = []
#     all_histories = []
    
#     for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
#         print(f"\nTraining Fold {fold + 1}/{n_splits}")
        
#         X_train, X_val = X[train_idx], X[val_idx]
#         y_train, y_val = y[train_idx], y[val_idx]
        
#         # Check for missing classes in training set
#         train_classes = np.unique(y_train)
#         val_classes = np.unique(y_val)
        
#         print(f"Training classes: {train_classes}")
#         print(f"Validation classes: {val_classes}")
        
#         # Create and train models for this fold
#         models = create_ensemble(input_shape, num_classes)
#         fold_predictions = []
        
#         for i, model in enumerate(models):
#             if isinstance(model, keras.Model):
#                 # Train deep learning model
#                 history = model.fit(
#                     X_train, y_train,
#                     validation_data=(X_val, y_val),
#                     epochs=100,
#                     batch_size=32,
#                     callbacks=[early_stopping, reduce_lr],
#                     verbose=1
#                 )
#                 all_histories.append(history)
#                 # Generate training graphs for this model
#                 generate_training_graphs(history, fold_num=fold+1, model_type=f"Model {i+1}")
#                 pred = model.predict(X_val)
#                 fold_predictions.append(pred)
#             else:
#                 # Train XGBoost model
#                 try:
#                     model.fit(X_train, y_train)
#                     pred = model.predict_proba(X_val)
#                     fold_predictions.append(pred)
#                 except Exception as e:
#                     print(f"XGBoost training failed: {e}")
#                     # Skip this model if training fails
#                     continue
        
#         # Average predictions for this fold
#         if fold_predictions:
#             fold_pred = np.mean(fold_predictions, axis=0)
#             fold_pred_classes = np.argmax(fold_pred, axis=1)
#             fold_accuracy = accuracy_score(y_val, fold_pred_classes)
#             fold_accuracies.append(fold_accuracy)
#             print(f"Fold {fold + 1} Accuracy: {fold_accuracy:.4f}")
            
#             ensemble_predictions.append((val_idx, fold_pred))
#         else:
#             print(f"Fold {fold + 1} skipped due to training failures")
    
#     return ensemble_predictions, np.mean(fold_accuracies) if fold_accuracies else 0, fold_accuracies, all_histories

# # Train the ensemble
# input_shape = (X_resampled.shape[1],)
# print(f"Input shape: {input_shape}")
# print(f"Number of classes: {num_classes}")

# ensemble_predictions, mean_accuracy, fold_accuracies, all_histories = train_ensemble(X_resampled, y_encoded, input_shape, num_classes)

# print(f"\nMean Cross-Validation Accuracy: {mean_accuracy:.4f}")

# # Save predictions and actual values
# final_predictions = np.zeros((len(X_resampled), num_classes))
# for idx, pred in ensemble_predictions:
#     final_predictions[idx] = pred

# # Final evaluation
# final_pred_classes = np.argmax(final_predictions, axis=1)
# final_accuracy = accuracy_score(y_encoded, final_pred_classes)
# print(f"Final Ensemble Accuracy: {final_accuracy:.4f}")

# # Generate evaluation graphs
# generate_evaluation_graphs(y_encoded, final_pred_classes, 
#                           label_encoder.classes_, fold_accuracies)

# # Print classification report
# print("\nClassification Report:")
# print(classification_report(y_encoded, final_pred_classes, 
#                           target_names=label_encoder.classes_))

# # Save the best model from the ensemble
# best_model = create_deep_model(input_shape, num_classes)
# best_model.compile(
#     optimizer=keras.optimizers.Adam(learning_rate=0.001),
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )

# # Train best model with validation split to get history
# best_history = best_model.fit(
#     X_resampled, y_encoded,
#     epochs=100,
#     batch_size=32,
#     callbacks=[early_stopping, reduce_lr],
#     validation_split=0.2,
#     verbose=1
# )

# # Generate graphs for the best model
# generate_training_graphs(best_history, model_type="Best Model")

# best_model.save('best_crop_model.keras')

# print("\nAll training and evaluation graphs have been generated and saved as PNG files.")


import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, PowerTransformer, RobustScaler
from sklearn.ensemble import VotingClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN
import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Load data
data = pd.read_csv('crop_dataset.csv')
target_column = 'Crop'

# Separate features and labels
X = data.drop(columns=[target_column])
y = data[target_column]

# Enhanced feature engineering
def create_interaction_features(X):
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            X[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-6)
            X[f'{col1}_{col2}_product'] = X[col1] * X[col2]
    return X

# Apply feature engineering
X = create_interaction_features(X)

# Categorical encoding
categorical_cols = X.select_dtypes(include=['object']).columns
X = pd.get_dummies(X, columns=categorical_cols)

# Feature selection
selector = SelectKBest(score_func=f_classif, k='all')
X_selected = selector.fit_transform(X, y)
selected_features_mask = selector.get_support()
selected_feature_names = X.columns[selected_features_mask].tolist()
X = X[selected_feature_names]

# Advanced preprocessing
def preprocess_features(X):
    power_transformer = PowerTransformer(method='yeo-johnson')
    robust_scaler = RobustScaler()
    
    # Apply both transformers
    X_power = power_transformer.fit_transform(X)
    X_robust = robust_scaler.fit_transform(X_power)
    
    return X_robust

X = preprocess_features(X)

# Enhanced sampling - FIX: Use regular SMOTE instead of SMOTEENN to preserve all classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Label encoding - Do this AFTER resampling to ensure consistent classes
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_resampled)

# Get the actual number of classes after resampling
num_classes = len(np.unique(y_encoded))
print(f"Number of classes after resampling: {num_classes}")
print(f"Class labels: {np.unique(y_encoded)}")

# Define deep learning model
def create_deep_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    
    # First block with skip connection
    x = Dense(512, kernel_regularizer=keras.regularizers.l2(0.01))(inputs)
    x = LeakyReLU(negative_slope=0.1)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    
    skip1 = x
    
    # Second block
    x = Dense(256, kernel_regularizer=keras.regularizers.l2(0.01))(x)
    x = LeakyReLU(negative_slope=0.1)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    
    # Add skip connection
    x = keras.layers.Concatenate()([x, skip1])
    
    # Third block
    x = Dense(128, kernel_regularizer=keras.regularizers.l2(0.01))(x)
    x = LeakyReLU(negative_slope=0.1)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    
    # Output
    outputs = Dense(num_classes, activation='softmax')(x)
    
    return keras.Model(inputs, outputs)

# Create ensemble of models
def create_ensemble(input_shape, num_classes, n_models=3):
    models = []
    
    for i in range(n_models):
        # Deep learning model
        dl_model = create_deep_model(input_shape, num_classes)
        dl_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        models.append(dl_model)
        
        # XGBoost model - FIXED: Use correct number of classes
        xgb_model = xgb.XGBClassifier(
            learning_rate=0.01,
            n_estimators=200,
            max_depth=7,
            min_child_weight=1,
            gamma=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='multi:softprob',
            num_class=num_classes,  # Use actual number of classes
            random_state=42+i
        )
        models.append(xgb_model)
    
    return models

# Callbacks for deep learning models
early_stopping = EarlyStopping(
    monitor='val_accuracy',
    patience=20,
    restore_best_weights=True,
    min_delta=0.001
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_accuracy',
    factor=0.2,
    patience=10,
    min_lr=1e-6,
    min_delta=0.001,
    verbose=1
)

# Function to generate training graphs
def generate_training_graphs(history, fold_num=None, model_type="Deep Learning"):
    """
    Generate comprehensive training graphs for model performance
    """
    if fold_num:
        title_suffix = f" - Fold {fold_num}"
    else:
        title_suffix = ""
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'{model_type} Training Performance{title_suffix}', fontsize=16, fontweight='bold')
    
    # Plot training & validation accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy', color='blue', linewidth=2)
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy', color='red', linewidth=2)
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot training & validation loss
    ax2.plot(history.history['loss'], label='Training Loss', color='blue', linewidth=2)
    ax2.plot(history.history['val_loss'], label='Validation Loss', color='red', linewidth=2)
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot learning rate
    if 'lr' in history.history:
        ax3.plot(history.history['lr'], label='Learning Rate', color='green', linewidth=2)
        ax3.set_title('Learning Rate Schedule')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Learning Rate')
        ax3.set_yscale('log')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    # Plot accuracy difference
    train_acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    acc_diff = [train_acc[i] - val_acc[i] for i in range(len(train_acc))]
    ax4.plot(acc_diff, label='Train-Val Accuracy Difference', color='purple', linewidth=2)
    ax4.axhline(y=0, color='black', linestyle='--', alpha=0.7)
    ax4.set_title('Training vs Validation Accuracy Difference')
    ax4.set_xlabel('Epoch')
    ax4.set_ylabel('Accuracy Difference')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'training_performance{title_suffix.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    plt.close()

# Function to generate evaluation graphs
def generate_evaluation_graphs(y_true, y_pred, class_names, fold_accuracies=None):
    """
    Generate evaluation graphs including confusion matrix and accuracy plots
    """
    # Create confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot accuracy per class
    class_accuracy = cm.diagonal() / cm.sum(axis=1)
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(class_names)), class_accuracy, color='skyblue', alpha=0.8)
    plt.title('Accuracy per Class', fontsize=16, fontweight='bold')
    plt.xlabel('Class')
    plt.ylabel('Accuracy')
    plt.xticks(range(len(class_names)), class_names, rotation=45, ha='right')
    plt.ylim(0, 1)
    
    # Add value labels on bars
    for bar, acc in zip(bars, class_accuracy):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{acc:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('class_accuracy.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot cross-validation fold accuracies if provided
    if fold_accuracies is not None:
        plt.figure(figsize=(10, 6))
        folds = range(1, len(fold_accuracies) + 1)
        plt.plot(folds, fold_accuracies, 'o-', color='green', linewidth=2, markersize=8)
        plt.axhline(y=np.mean(fold_accuracies), color='red', linestyle='--', 
                   label=f'Mean Accuracy: {np.mean(fold_accuracies):.4f}')
        plt.title('Cross-Validation Fold Accuracies', fontsize=16, fontweight='bold')
        plt.xlabel('Fold Number')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(folds)
        plt.ylim(0, 1)
        
        # Add value labels on points
        for i, acc in enumerate(fold_accuracies):
            plt.text(folds[i], acc + 0.01, f'{acc:.4f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('cv_accuracy.png', dpi=300, bbox_inches='tight')
        plt.close()

# Training with k-fold cross validation - FIX: Use StratifiedKFold instead of KFold
n_splits = 5
kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# Train ensemble
def train_ensemble(X, y, input_shape, num_classes):
    ensemble_predictions = []
    fold_accuracies = []
    all_histories = []
    
    for fold, (train_idx, val_idx) in enumerate(kf.split(X, y)):
        print(f"\nTraining Fold {fold + 1}/{n_splits}")
        
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        # Create and train models for this fold
        models = create_ensemble(input_shape, num_classes)
        fold_predictions = []
        
        for i, model in enumerate(models):
            if isinstance(model, keras.Model):
                # Train deep learning model
                history = model.fit(
                    X_train, y_train,
                    validation_data=(X_val, y_val),
                    epochs=100,
                    batch_size=32,
                    callbacks=[early_stopping, reduce_lr],
                    verbose=1
                )
                all_histories.append(history)
                # Generate training graphs for this model
                generate_training_graphs(history, fold_num=fold+1, model_type=f"Model {i+1}")
                pred = model.predict(X_val)
                fold_predictions.append(pred)
            else:
                # Train XGBoost model - FIXED: Simplified approach
                try:
                    model.fit(X_train, y_train)
                    pred = model.predict_proba(X_val)
                    fold_predictions.append(pred)
                except Exception as e:
                    print(f"XGBoost training failed: {e}")
                    # Skip this model if training fails
                    continue
        
        # Average predictions for this fold
        if fold_predictions:
            fold_pred = np.mean(fold_predictions, axis=0)
            fold_pred_classes = np.argmax(fold_pred, axis=1)
            fold_accuracy = accuracy_score(y_val, fold_pred_classes)
            fold_accuracies.append(fold_accuracy)
            print(f"Fold {fold + 1} Accuracy: {fold_accuracy:.4f}")
            
            ensemble_predictions.append((val_idx, fold_pred))
        else:
            print(f"Fold {fold + 1} skipped due to training failures")
    
    return ensemble_predictions, np.mean(fold_accuracies) if fold_accuracies else 0, fold_accuracies, all_histories

# Train the ensemble
input_shape = (X_resampled.shape[1],)
print(f"Input shape: {input_shape}")
print(f"Number of classes: {num_classes}")

ensemble_predictions, mean_accuracy, fold_accuracies, all_histories = train_ensemble(X_resampled, y_encoded, input_shape, num_classes)

print(f"\nMean Cross-Validation Accuracy: {mean_accuracy:.4f}")

# Save predictions and actual values
final_predictions = np.zeros((len(X_resampled), num_classes))
for idx, pred in ensemble_predictions:
    final_predictions[idx] = pred

# Final evaluation
final_pred_classes = np.argmax(final_predictions, axis=1)
final_accuracy = accuracy_score(y_encoded, final_pred_classes)
print(f"Final Ensemble Accuracy: {final_accuracy:.4f}")

# Generate evaluation graphs
generate_evaluation_graphs(y_encoded, final_pred_classes, 
                          label_encoder.classes_, fold_accuracies)

# Print classification report
print("\nClassification Report:")
print(classification_report(y_encoded, final_pred_classes, 
                          target_names=label_encoder.classes_))

# Save the best model from the ensemble
best_model = create_deep_model(input_shape, num_classes)
best_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train best model with validation split to get history
best_history = best_model.fit(
    X_resampled, y_encoded,
    epochs=100,
    batch_size=32,
    callbacks=[early_stopping, reduce_lr],
    validation_split=0.2,
    verbose=1
)

# Generate graphs for the best model
generate_training_graphs(best_history, model_type="Best Model")

best_model.save('best_crop_model.keras')

print("\nAll training and evaluation graphs have been generated and saved as PNG files.")