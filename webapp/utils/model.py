"""
utils/model.py — Model loading and prediction logic.
"""
import numpy as np
import pandas as pd
import joblib
import os
import streamlit as st

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')


@st.cache_resource
def load_models():
    """Load all ML models and artifacts (cached)."""
    xgb_model = joblib.load(os.path.join(MODELS_DIR, 'xgboost_4class.pkl'))
    mlp_model = joblib.load(os.path.join(MODELS_DIR, 'mlp_4class.pkl'))
    le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder_4class.pkl'))
    stats = joblib.load(os.path.join(MODELS_DIR, 'feature_stats.pkl'))
    return xgb_model, mlp_model, le, stats


def predict_class(X_scaled, model_name='xgboost'):
    """
    Predict performance class for a scaled feature array.
    Returns (class_label, probabilities_dict, class_index).
    """
    xgb_model, mlp_model, le, _ = load_models()
    model = xgb_model if model_name == 'xgboost' else mlp_model

    pred = model.predict(X_scaled)
    proba = model.predict_proba(X_scaled)

    class_label = le.inverse_transform(pred)[0]
    proba_dict = {le.inverse_transform([i])[0]: float(proba[0][i]) for i in range(len(le.classes_))}
    return class_label, proba_dict, int(pred[0])


@st.cache_resource(show_spinner=False)
def get_custom_model(model_name, **kwargs):
    """Train a model on the fly based on user-provided hyperparameters."""
    import pandas as pd
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    from sklearn.neural_network import MLPClassifier
    import xgboost as xgb
    
    df = pd.read_csv(os.path.join(MODELS_DIR, 'cleaned_data.csv'))
    feature_cols = joblib.load(os.path.join(MODELS_DIR, 'feature_cols.pkl'))
    X = df[feature_cols].values
    
    scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
    le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder_4class.pkl'))
    
    X_scaled = scaler.transform(X)
    y = le.transform(df['performanceClass'])
    
    if model_name == 'KNN':
        model = KNeighborsClassifier(n_neighbors=kwargs.get('n_neighbors', 7))
    elif model_name == 'Decision Tree':
        model = DecisionTreeClassifier(max_depth=kwargs.get('max_depth', 9), random_state=42)
    elif model_name == 'SVM (Linear)':
        model = SVC(kernel='linear', C=kwargs.get('C', 1.0), probability=True, random_state=42)
    elif model_name == 'SVM (RBF)':
        gamma = kwargs.get('gamma', 0.1)
        model = SVC(kernel='rbf', C=kwargs.get('C', 10.0), gamma=gamma if gamma != 0.0 else 'scale', probability=True, random_state=42)
    elif model_name == 'MLP':
        layer1 = kwargs.get('hidden_layer_1', 128)
        layer2 = kwargs.get('hidden_layer_2', 64)
        layers = (layer1, layer2) if layer2 > 0 else (layer1,)
        model = MLPClassifier(hidden_layer_sizes=layers, activation='relu',
                               solver='adam', alpha=kwargs.get('alpha', 0.001), 
                               max_iter=kwargs.get('max_iter', 200), random_state=42)
    elif model_name == 'XGBoost':
        model = xgb.XGBClassifier(n_estimators=kwargs.get('n_estimators', 100), 
                                  max_depth=kwargs.get('max_depth', 6), 
                                  learning_rate=kwargs.get('learning_rate', 0.1),
                                  random_state=42, eval_metric='mlogloss', verbosity=0)
    else:
        model = xgb.XGBClassifier()
        
    model.fit(X_scaled, y)
    return model

def predict_custom_class(X_scaled, custom_model):
    """Predict performance class using a user-trained custom model."""
    xgb_model, mlp_model, le, _ = load_models()
    
    pred = custom_model.predict(X_scaled)
    proba = custom_model.predict_proba(X_scaled)

    class_label = le.inverse_transform(pred)[0]
    proba_dict = {le.inverse_transform([i])[0]: float(proba[0][i]) for i in range(len(le.classes_))}
    return class_label, proba_dict, int(pred[0])

def predict_batch(X_scaled, model_name='xgboost'):
    """
    Batch predict for CSV upload.
    Returns (class_labels_array, probabilities_array).
    """
    xgb_model, mlp_model, le, _ = load_models()
    model = xgb_model if model_name == 'xgboost' else mlp_model

    preds = model.predict(X_scaled)
    probas = model.predict_proba(X_scaled)

    labels = le.inverse_transform(preds)
    return labels, probas


def get_class_info(class_label):
    """Get metadata for a performance class."""
    info = {
        'A': {
            'name': 'Elite Performer',
            'emoji': '🏆',
            'color': '#10B981',
            'gradient': 'linear-gradient(135deg, #10B981, #059669)',
            'description': 'Outstanding! You\'re in the top tier of physical fitness. Your body performs at an elite level across strength, endurance, and flexibility.',
            'level': 4,
        },
        'B': {
            'name': 'Strong Performer', 
            'emoji': '💪',
            'color': '#3B82F6',
            'gradient': 'linear-gradient(135deg, #3B82F6, #2563EB)',
            'description': 'Great job! You\'re above average with solid fitness foundations. A few targeted improvements can push you to elite status.',
            'level': 3,
        },
        'C': {
            'name': 'Average Performer',
            'emoji': '🎯',
            'color': '#F59E0B',
            'gradient': 'linear-gradient(135deg, #F59E0B, #D97706)',
            'description': 'You\'re in the middle range. There\'s significant room for improvement in key areas. A consistent plan will yield noticeable results.',
            'level': 2,
        },
        'D': {
            'name': 'Needs Improvement',
            'emoji': '🌱',
            'color': '#EF4444',
            'gradient': 'linear-gradient(135deg, #EF4444, #DC2626)',
            'description': 'Your fitness needs attention, but everyone starts somewhere! With the right guidance, you\'ll see dramatic improvements quickly.',
            'level': 1,
        },
    }
    return info.get(class_label, info['C'])
