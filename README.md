# 🏋️‍♂️ Body Performance Classification & Predictive Analytics

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-XGBoost%20%7C%20Scikit--Learn-orange)](#)
[![Streamlit App](https://img.shields.io/badge/Web%20App-Streamlit-FF4B4B)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Live Demo:** *(Add your Streamlit Cloud link here)*

## 📌 Project Overview
This project applies end-to-end Machine Learning to classify human physiological performance based on demographic and biomechanical metrics. Using a dataset of 13,393 individuals, we developed a robust classification pipeline to categorize individuals into performance tiers, achieving **89% accuracy on binary classification** and **83.4% on a 3-tier health risk assessment** using a tuned **XGBoost** model.

## 🎯 Business Value
Fitness and health insurance industries rely on rapid, non-invasive measurements to assess mortality risk and physical capability. This project demonstrates how standard anthropometric data (age, BMI, blood pressure) combined with simple kinetic tests (grip strength, broad jump) can highly accurately predict a patient's overall physical competence, potentially reducing the need for expensive VO2 Max or DEXA scan testing in preliminary screenings.

## 📊 Dataset
The [Body Performance Dataset (Kaggle)](https://www.kaggle.com/) contains 13,393 records with 12 features:
*   **Demographics:** Age, Gender
*   **Anthropometrics:** Height, Weight, Body Fat %
*   **Cardiovascular:** Systolic/Diastolic Blood Pressure
*   **Kinetics/Fitness:** Grip Force, Sit & Bend (Flexibility), Sit-ups (Endurance), Broad Jump (Power)
*   **Target:** Performance Class (A, B, C, D)

## 🛠️ Methodology & Tech Stack
1.  **Data Processing & EDA (`pandas`, `seaborn`):** Handled extreme physiological outliers, resolved data entry errors (e.g., diastolic > systolic), and analyzed biomechanical decay across age groups.
2.  **Feature Engineering:** Engineered interaction terms (`gripPerLeanMass`, `genderXgrip`) and normalized metrics (`sitUpsCounts_zGender`) to control for biological sex baseline differences.
3.  **Modeling Pipeline (`scikit-learn`, `xgboost`):** Evaluated KNN, SVM, Decision Trees, MLP, and XGBoost. Implemented strict Scikit-Learn `Pipeline` architectures to prevent data leakage during 5-Fold Stratified Cross-Validation.
4.  **Interpretability (`SHAP`):** Utilized SHAP tree explainers to extract feature importance, proving that core endurance (sit-ups) and explosive power (broad jump) are the strongest predictors of overall class.
5.  **Deployment (`Streamlit`):** Packaged the inference pipeline into an interactive web dashboard for real-time predictions.

## 🚀 Key Results
*   **XGBoost** emerged as the superior model, heavily outperforming distance-based models (KNN, SVM) which struggled with the overlapping distributions of Classes B and C.
*   **4-Class Accuracy:** 77.5%
*   **3-Class Accuracy (High / Average / Low):** 83.4%
*   **Binary Class Accuracy (Good / Poor):** 89.0%

## 💻 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YourUsername/body-performance-ml.git
cd body-performance-ml

# 2. Create a virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit Web App
cd webapp
streamlit run app.py
```

## 📂 Project Structure

```text
body-performance-ml/
│
├── data/
│   ├── raw/                # Original dataset
│   └── processed/          # Cleaned dataset ready for modeling
│
├── notebooks/
│   ├── 01_DataPreparation_EDA.ipynb        # Data cleaning and visualizations
│   └── 02_ModelTraining_Evaluation.ipynb   # Machine Learning pipeline
│
├── webapp/                 # Streamlit application source code
│
├── reports/                
│   ├── figures/            # Curated plots and SHAP summary
│   └── Final_Report.md     # Detailed analytical report
│
├── .gitignore              # Ignored files
├── requirements.txt        # Core dependencies
└── README.md               # Project documentation
```

## 🔮 Future Improvements
*   Implement SMOTE for synthetic balancing if specific age brackets become highly imbalanced.
*   Containerize the web application using Docker.
*   Transition from local CSV to a cloud SQL database for live data ingestion.
