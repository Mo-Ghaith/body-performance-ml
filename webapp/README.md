# 🏋️ Body Performance AI

AI-powered fitness analysis web application built with **Streamlit**, powered by **XGBoost** and **MLP Neural Networks**.

![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)

## ✨ Features

- **🎯 AI Prediction** — Enter body metrics and get instant performance classification (A/B/C/D)
- **🥗 Personalized Diet Plans** — Custom nutrition guidance based on your fitness level
- **💪 Exercise Programs** — Tailored strength, flexibility, and cardio routines
- **📊 Interactive Dashboard** — Explore 13,000+ records with Plotly charts
- **📁 CSV Batch Upload** — Upload CSV files for bulk predictions with downloadable results
- **🔬 What-If Simulator** — Adjust metrics and see real-time prediction changes

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Train & Export Models

```bash
python train_and_export.py
```

This trains XGBoost and MLP models and saves them to the `models/` directory.

### 3. Run the App

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 📁 Project Structure

```
├── app.py                    # Main Streamlit landing page
├── pages/
│   ├── 1_🏋️_Predict.py       # Individual prediction form
│   ├── 2_📊_Dashboard.py      # Dataset visualizations
│   ├── 3_📁_CSV_Upload.py     # Batch CSV prediction  
│   ├── 4_🔬_Simulator.py      # What-if scenario tool
│   ├── 5_🥗_Diet_Plans.py     # Dietary recommendations
│   └── 6_💪_Exercise_Programs.py # Customized workout routines
├── utils/
│   ├── model.py              # ML model loading & prediction
│   ├── preprocessing.py      # Feature engineering pipeline
│   ├── recommendations.py    # Diet/exercise plan generator
│   └── charts.py             # Plotly chart helpers
├── train_and_export.py       # Model training script
├── models/                   # Saved model artifacts
├── data/
│   └── sample_input.csv      # Example CSV for testing
├── assets/
│   └── style.css             # Premium dark theme CSS
└── README.md
```

## 🤖 Models

| Model | Type | Accuracy (4-class) |
|-------|------|-------------------|
| XGBoost | Ensemble | ~73% |
| MLP (128,64) | Neural Network | ~70% |

## 📊 Dataset

[Kaggle Body Performance Dataset](https://www.kaggle.com/datasets/kukuroo3/body-performance-data) — 13,393 records with 12 features measuring physical fitness.

## 📝 License

This project is for educational purposes.
