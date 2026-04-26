"""
utils/preprocessing.py — Feature engineering and preprocessing for single and batch inputs.
"""
import numpy as np
import pandas as pd
import joblib
import os

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')


def _load_artifacts():
    """Load scaler, feature columns, and gender sit-up stats."""
    scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
    feature_cols = joblib.load(os.path.join(MODELS_DIR, 'feature_cols.pkl'))
    gender_stats = joblib.load(os.path.join(MODELS_DIR, 'gender_situp_stats.pkl'))
    return scaler, feature_cols, gender_stats


def _engineer_row(row, gender_stats):
    """Add engineered features to a single-row dict or Series."""
    row = dict(row)
    row['genderEncoded'] = 1 if row.get('gender', 'M') == 'M' else 0
    height_m = row['heightCm'] / 100
    row['bmi'] = row['weightKg'] / (height_m ** 2)

    # Gender-normalized sit-ups z-score
    g = row.get('gender', 'M')
    mean_val = gender_stats['mean'].get(g, gender_stats['mean'].get('M', 40))
    std_val = gender_stats['std'].get(g, gender_stats['std'].get('M', 15))
    if std_val == 0:
        std_val = 1
    row['sitUpsCounts_zGender'] = (row['sitUpsCounts'] - mean_val) / std_val

    # Grip per lean mass
    lean_mass = row['weightKg'] * (1 - row['bodyFatPercent'] / 100)
    if lean_mass <= 0:
        lean_mass = 1
    row['gripPerLeanMass'] = row['gripForce'] / lean_mass

    # Gender x grip interaction
    row['genderXgrip'] = row['genderEncoded'] * row['gripForce']
    return row


def preprocess_single(data_dict):
    """
    Take a dict of raw user inputs and return a scaled feature array ready for prediction.
    
    Expected keys: age, gender, heightCm, weightKg, bodyFatPercent, diastolic, systolic,
                   gripForce, sitAndBendForwardCm, sitUpsCounts, broadJumpCm
    """
    scaler, feature_cols, gender_stats = _load_artifacts()
    row = _engineer_row(data_dict, gender_stats)
    features = np.array([[row[col] for col in feature_cols]])
    return scaler.transform(features)


def preprocess_csv(df):
    """
    Take a DataFrame with raw columns and return (scaled_array, processed_df).
    
    Accepts both original column names (from Kaggle) and renamed camelCase columns.
    """
    scaler, feature_cols, gender_stats = _load_artifacts()

    # Map original column names to camelCase if needed
    rename_map = {
        'height_cm': 'heightCm', 'weight_kg': 'weightKg',
        'body fat_%': 'bodyFatPercent',
        'sit and bend forward_cm': 'sitAndBendForwardCm',
        'sit-ups counts': 'sitUpsCounts',
        'broad jump_cm': 'broadJumpCm',
        'class': 'performanceClass',
    }
    df = df.rename(columns=rename_map)

    processed_rows = []
    for _, row in df.iterrows():
        processed_rows.append(_engineer_row(row.to_dict(), gender_stats))

    processed_df = pd.DataFrame(processed_rows)
    features = processed_df[feature_cols].values
    scaled = scaler.transform(features)
    return scaled, processed_df
