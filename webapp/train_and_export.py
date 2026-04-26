"""
train_and_export.py — Train models from the BodyPerformance dataset and export them for the web app.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import joblib
import os

def clean_data(df):
    """Apply the same cleaning pipeline from the EDA notebook."""
    # Fix 1: Diastolic >= Systolic
    df = df[df['diastolic'] < df['systolic']]
    # Fix 2: Extreme body fat
    mask = (
        (df['body fat_%'] < 5) |
        (df['body fat_%'] > 50) |
        ((df['gender'] == 'F') & (df['body fat_%'] < 10)) |
        ((df['gender'] == 'M') & (df['body fat_%'] > 45))
    )
    df = df[~mask]
    # Fix 3: Zero values
    mask_jump = df['broad jump_cm'] == 0
    mask_grip = df['gripForce'] == 0
    mask_bp = (df['systolic'] == 0) | (df['diastolic'] == 0)
    mask_sit = (df['sit-ups counts'] == 0) & (df['age'] < 60)
    df = df[~(mask_jump | mask_grip | mask_bp | mask_sit)]
    # Fix 4: Sit-and-bend range
    mask = (df['sit and bend forward_cm'] < -30) | (df['sit and bend forward_cm'] > 50)
    df = df[~mask]
    # Fix 5: Very low diastolic
    df = df[df['diastolic'] >= 20]
    # Fix 6: Extreme BMI
    bmi = df['weight_kg'] / (df['height_cm'] / 100) ** 2
    df = df[bmi >= 14]
    # Fix 7: Broad jump > 290
    df = df[df['broad jump_cm'] <= 290]
    # Rename columns
    rename_map = {
        'age': 'age', 'gender': 'gender',
        'height_cm': 'heightCm', 'weight_kg': 'weightKg',
        'body fat_%': 'bodyFatPercent',
        'diastolic': 'diastolic', 'systolic': 'systolic',
        'gripForce': 'gripForce',
        'sit and bend forward_cm': 'sitAndBendForwardCm',
        'sit-ups counts': 'sitUpsCounts',
        'broad jump_cm': 'broadJumpCm',
        'class': 'performanceClass',
    }
    df = df.rename(columns=rename_map)
    df = df.reset_index(drop=True)
    return df


def engineer_features(df):
    """Create the 4 engineered features matching the ML notebook."""
    df = df.copy()
    df['genderEncoded'] = (df['gender'] == 'M').astype(int)
    df['bmi'] = df['weightKg'] / (df['heightCm'] / 100) ** 2
    # Gender-normalized sit-ups z-score
    gender_situp_stats = df.groupby('gender')['sitUpsCounts'].agg(['mean', 'std']).to_dict()
    df['sitUpsCounts_zGender'] = df.groupby('gender')['sitUpsCounts'].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    # Grip per lean mass
    lean_mass = df['weightKg'] * (1 - df['bodyFatPercent'] / 100)
    df['gripPerLeanMass'] = df['gripForce'] / lean_mass
    # Gender x grip interaction
    df['genderXgrip'] = df['genderEncoded'] * df['gripForce']
    return df, gender_situp_stats


def main():
    print("=" * 60)
    print("  TRAINING & EXPORTING MODELS")
    print("=" * 60)

    # Load raw data
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw', 'bodyPerformance.csv')
    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found!")
        return
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows")

    # Clean
    df = clean_data(df)
    print(f"After cleaning: {len(df)} rows")

    # Engineer features
    df, gender_situp_stats = engineer_features(df)

    # Feature columns (must match notebook order exactly)
    feature_cols = [
        'age', 'heightCm', 'weightKg', 'bodyFatPercent', 'diastolic',
        'systolic', 'gripForce', 'sitAndBendForwardCm', 'sitUpsCounts',
        'broadJumpCm', 'genderEncoded',
        'bmi', 'sitUpsCounts_zGender', 'gripPerLeanMass', 'genderXgrip'
    ]

    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4-class target
    le4 = LabelEncoder()
    y4 = le4.fit_transform(df['performanceClass'])
    print(f"Classes: {list(le4.classes_)}")

    # Split
    Xtr, Xte, ytr, yte = train_test_split(X_scaled, y4, test_size=0.2, random_state=42, stratify=y4)

    # --- Train XGBoost ---
    print("\nTraining XGBoost...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=500, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0, min_child_weight=5,
        random_state=42, eval_metric='mlogloss', verbosity=0
    )
    xgb_model.fit(Xtr, ytr)
    acc_xgb = xgb_model.score(Xte, yte)
    print(f"  XGBoost Accuracy: {acc_xgb:.4f}")

    # --- Train MLP ---
    print("Training MLP...")
    mlp_model = MLPClassifier(
        hidden_layer_sizes=(128, 64), activation='relu',
        solver='adam', alpha=0.001, max_iter=500,
        random_state=42, early_stopping=True,
        validation_fraction=0.1, batch_size=128
    )
    mlp_model.fit(Xtr, ytr)
    acc_mlp = mlp_model.score(Xte, yte)
    print(f"  MLP Accuracy: {acc_mlp:.4f}")

    # --- Save everything ---
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)

    joblib.dump(xgb_model, os.path.join(models_dir, 'xgboost_4class.pkl'))
    joblib.dump(mlp_model, os.path.join(models_dir, 'mlp_4class.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(le4, os.path.join(models_dir, 'label_encoder_4class.pkl'))
    joblib.dump(feature_cols, os.path.join(models_dir, 'feature_cols.pkl'))
    joblib.dump(gender_situp_stats, os.path.join(models_dir, 'gender_situp_stats.pkl'))

    # Save dataset statistics for the dashboard
    stats = {
        'means': df[feature_cols].mean().to_dict(),
        'stds': df[feature_cols].std().to_dict(),
        'mins': df[feature_cols].min().to_dict(),
        'maxs': df[feature_cols].max().to_dict(),
        'class_means': df.groupby('performanceClass')[feature_cols].mean().to_dict(),
    }
    joblib.dump(stats, os.path.join(models_dir, 'feature_stats.pkl'))

    # Save cleaned dataset for dashboard
    df.to_csv(os.path.join(models_dir, 'cleaned_data.csv'), index=False)

    print(f"\n[OK] All models and artifacts saved to {models_dir}/")
    print("  - xgboost_4class.pkl")
    print("  - mlp_4class.pkl")
    print("  - scaler.pkl")
    print("  - label_encoder_4class.pkl")
    print("  - feature_cols.pkl")
    print("  - gender_situp_stats.pkl")
    print("  - feature_stats.pkl")
    print("  - cleaned_data.csv")


if __name__ == '__main__':
    main()
