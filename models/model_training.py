"""
AI MedAssist - ML Model Training Script
Trains Random Forest and XGBoost classifiers on the disease-symptom dataset.
Saves trained models and encoders as pickle files.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, '..', 'dataset', 'disease_dataset.csv')
MODEL_DIR = BASE_DIR  # Save models in this directory

# ──────────────────────────────────────────────
# 1. Load and preprocess data
# ──────────────────────────────────────────────
print("[1/6] Loading dataset...")
df = pd.read_csv(DATASET_PATH)
print(f"  ➜ Loaded {len(df)} samples with {df['Disease'].nunique()} diseases")

# Collect all unique symptoms
symptom_columns = [col for col in df.columns if col.startswith('Symptom')]
all_symptoms = set()
for col in symptom_columns:
    all_symptoms.update(df[col].dropna().unique())
all_symptoms = sorted(list(all_symptoms))
print(f"  ➜ Found {len(all_symptoms)} unique symptoms")

# ──────────────────────────────────────────────
# 2. Create binary feature matrix
# ──────────────────────────────────────────────
print("[2/6] Creating feature matrix...")

def symptoms_to_vector(row, symptom_list):
    """Convert a row of symptom columns into a binary vector."""
    vector = np.zeros(len(symptom_list))
    for col in symptom_columns:
        symptom = row[col]
        if pd.notna(symptom) and symptom in symptom_list:
            idx = symptom_list.index(symptom)
            vector[idx] = 1
    return vector

X = np.array([symptoms_to_vector(row, all_symptoms) for _, row in df.iterrows()])

# Encode disease labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['Disease'])

print(f"  ➜ Feature matrix shape: {X.shape}")
print(f"  ➜ Classes: {list(label_encoder.classes_)}")

# ──────────────────────────────────────────────
# 3. Split data
# ──────────────────────────────────────────────
print("[3/6] Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"  ➜ Training: {X_train.shape[0]}, Testing: {X_test.shape[0]}")

# ──────────────────────────────────────────────
# 4. Train Random Forest
# ──────────────────────────────────────────────
print("[4/6] Training Random Forest Classifier...")
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
print(f"  ➜ Random Forest Accuracy: {rf_accuracy:.4f}")

# Cross-validation
rf_cv_scores = cross_val_score(rf_model, X, y, cv=5)
print(f"  ➜ CV Score (5-fold): {rf_cv_scores.mean():.4f} ± {rf_cv_scores.std():.4f}")

# ──────────────────────────────────────────────
# 5. Train XGBoost
# ──────────────────────────────────────────────
print("[5/6] Training XGBoost Classifier...")
xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=10,
    learning_rate=0.1,
    random_state=42,
    use_label_encoder=False,
    eval_metric='mlogloss',
    n_jobs=-1
)
xgb_model.fit(X_train, y_train)

xgb_pred = xgb_model.predict(X_test)
xgb_accuracy = accuracy_score(y_test, xgb_pred)
print(f"  ➜ XGBoost Accuracy: {xgb_accuracy:.4f}")

xgb_cv_scores = cross_val_score(xgb_model, X, y, cv=5)
print(f"  ➜ CV Score (5-fold): {xgb_cv_scores.mean():.4f} ± {xgb_cv_scores.std():.4f}")

# ──────────────────────────────────────────────
# 6. Save models and metadata
# ──────────────────────────────────────────────
print("[6/6] Saving models and metadata...")

# Save models
joblib.dump(rf_model, os.path.join(MODEL_DIR, 'random_forest_model.pkl'))
joblib.dump(xgb_model, os.path.join(MODEL_DIR, 'xgboost_model.pkl'))
joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'label_encoder.pkl'))

# Save symptom list as JSON for frontend/backend usage
symptom_metadata = {
    'symptoms': all_symptoms,
    'diseases': list(label_encoder.classes_),
    'rf_accuracy': float(rf_accuracy),
    'xgb_accuracy': float(xgb_accuracy),
    'total_samples': len(df),
    'total_symptoms': len(all_symptoms),
    'total_diseases': len(label_encoder.classes_)
}
with open(os.path.join(MODEL_DIR, 'model_metadata.json'), 'w') as f:
    json.dump(symptom_metadata, f, indent=2)

# Save disease precautions
precautions = {
    "Influenza": [
        "Rest for 8-10 hours daily",
        "Increase fluid intake (water, herbal tea)",
        "Wear a mask and avoid public spaces",
        "Take prescribed antiviral medications",
        "Monitor temperature regularly"
    ],
    "Common Cold": [
        "Stay hydrated with warm fluids",
        "Use saline nasal drops",
        "Get adequate rest",
        "Gargle with warm salt water",
        "Use a humidifier"
    ],
    "Diabetes": [
        "Monitor blood sugar levels regularly",
        "Follow a low-sugar, balanced diet",
        "Exercise for at least 30 minutes daily",
        "Take insulin or medications as prescribed",
        "Schedule regular check-ups"
    ],
    "Hypertension": [
        "Reduce sodium intake",
        "Exercise regularly",
        "Manage stress through meditation",
        "Take prescribed blood pressure medication",
        "Avoid alcohol and smoking"
    ],
    "Malaria": [
        "Use mosquito nets while sleeping",
        "Take antimalarial medication as prescribed",
        "Stay hydrated",
        "Rest adequately",
        "Seek immediate medical attention if symptoms worsen"
    ],
    "Typhoid": [
        "Drink only purified water",
        "Maintain strict hygiene",
        "Take antibiotics as prescribed",
        "Eat freshly prepared food",
        "Rest completely until recovery"
    ],
    "Dengue": [
        "Stay hydrated with ORS and fluids",
        "Monitor platelet count regularly",
        "Use mosquito repellent",
        "Avoid aspirin and ibuprofen",
        "Seek hospital care if symptoms worsen"
    ],
    "Pneumonia": [
        "Take prescribed antibiotics completely",
        "Rest and stay hydrated",
        "Use a humidifier",
        "Avoid smoking and secondhand smoke",
        "Get a pneumococcal vaccine"
    ],
    "Tuberculosis": [
        "Complete the full course of TB medication",
        "Maintain good ventilation at home",
        "Cover mouth when coughing",
        "Get regular sputum tests",
        "Eat nutritious food for recovery"
    ],
    "Asthma": [
        "Carry a rescue inhaler at all times",
        "Avoid known triggers (dust, smoke, pollen)",
        "Use prescribed controller medications",
        "Monitor peak flow readings",
        "Create an asthma action plan with your doctor"
    ],
    "Gastroenteritis": [
        "Stay hydrated with ORS solutions",
        "Eat bland, easy-to-digest foods",
        "Wash hands frequently",
        "Avoid dairy products temporarily",
        "Rest until symptoms subside"
    ],
    "Migraine": [
        "Rest in a dark, quiet room",
        "Apply cold or warm compresses",
        "Stay hydrated",
        "Take prescribed migraine medication early",
        "Identify and avoid personal triggers"
    ],
    "Anemia": [
        "Eat iron-rich foods (spinach, red meat, beans)",
        "Take iron supplements as prescribed",
        "Include vitamin C to improve iron absorption",
        "Get regular blood tests",
        "Avoid tea/coffee with meals"
    ],
    "Jaundice": [
        "Rest completely",
        "Follow a high-carbohydrate, low-fat diet",
        "Avoid alcohol completely",
        "Stay hydrated",
        "Take prescribed medications regularly"
    ],
    "Urinary Tract Infection": [
        "Drink plenty of water",
        "Take prescribed antibiotics fully",
        "Maintain personal hygiene",
        "Avoid irritating feminine products",
        "Urinate frequently, don't hold it in"
    ],
    "Chickenpox": [
        "Keep the rash clean and dry",
        "Use calamine lotion for itching",
        "Avoid scratching blisters",
        "Stay isolated until blisters crust over",
        "Take prescribed antiviral medication"
    ],
    "Arthritis": [
        "Exercise regularly with low-impact activities",
        "Apply hot/cold therapy to joints",
        "Maintain a healthy weight",
        "Take anti-inflammatory medications as prescribed",
        "Consider physical therapy"
    ],
    "Bronchitis": [
        "Rest and drink plenty of fluids",
        "Use a humidifier",
        "Avoid smoking and irritants",
        "Take prescribed cough suppressants",
        "Use prescribed inhalers if needed"
    ],
    "Sinusitis": [
        "Use saline nasal irrigation",
        "Apply warm compresses to the face",
        "Stay hydrated",
        "Use prescribed nasal corticosteroids",
        "Avoid allergens and irritants"
    ],
    "Allergic Rhinitis": [
        "Avoid known allergens",
        "Use antihistamine medications",
        "Keep windows closed during high pollen days",
        "Use air purifiers indoors",
        "Consider allergy immunotherapy"
    ],
    "Conjunctivitis": [
        "Wash hands frequently",
        "Avoid touching eyes",
        "Use prescribed eye drops",
        "Don't share towels or pillows",
        "Replace contact lenses and makeup"
    ],
    "Food Poisoning": [
        "Stay hydrated with clear fluids",
        "Eat bland foods when able to eat",
        "Avoid dairy and spicy foods",
        "Wash hands thoroughly",
        "Seek medical help if symptoms persist 48+ hours"
    ],
    "Heart Disease": [
        "Follow a heart-healthy diet",
        "Exercise regularly as advised by doctor",
        "Take all prescribed medications",
        "Monitor blood pressure and cholesterol",
        "Quit smoking immediately"
    ],
    "Kidney Disease": [
        "Follow a kidney-friendly diet (low sodium, potassium)",
        "Stay hydrated but don't overdrink",
        "Take prescribed medications regularly",
        "Monitor blood pressure",
        "Get regular kidney function tests"
    ],
    "Hepatitis": [
        "Avoid alcohol completely",
        "Rest adequately",
        "Eat a nutritious diet",
        "Take prescribed antiviral medications",
        "Practice safe hygiene to prevent spread"
    ],
    "COVID-19": [
        "Isolate for recommended period",
        "Monitor oxygen levels with a pulse oximeter",
        "Stay hydrated and rest",
        "Take prescribed medications",
        "Seek emergency care if breathing difficulty worsens"
    ],
    "Thyroid Disorder": [
        "Take thyroid medication as prescribed",
        "Get regular thyroid function tests",
        "Maintain a balanced diet with iodine",
        "Exercise regularly",
        "Monitor weight changes"
    ],
    "Appendicitis": [
        "Seek immediate emergency medical care",
        "Do not eat or drink before surgery",
        "Surgery (appendectomy) is usually required",
        "Follow post-surgery care instructions",
        "Watch for signs of infection after surgery"
    ],
    "Meningitis": [
        "Seek immediate emergency medical treatment",
        "Take prescribed antibiotics/antivirals",
        "Rest in a quiet, dark room",
        "Stay hydrated",
        "Get vaccinated for prevention"
    ]
}
with open(os.path.join(MODEL_DIR, 'disease_precautions.json'), 'w') as f:
    json.dump(precautions, f, indent=2)

print("\n" + "=" * 50)
print("✅ Model training complete!")
print(f"  📁 Models saved to: {MODEL_DIR}")
print(f"  🌳 Random Forest Accuracy: {rf_accuracy:.2%}")
print(f"  🚀 XGBoost Accuracy:       {xgb_accuracy:.2%}")
print(f"  🔢 Total Symptoms:         {len(all_symptoms)}")
print(f"  🏥 Total Diseases:          {len(label_encoder.classes_)}")
print("=" * 50)
