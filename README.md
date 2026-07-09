# 🧠 AI Medical Based Diagnosis Assitant Using Machine Learning

This is a smart healthcare web application that predicts diseases based on symptoms using Machine Learning.

---

## 🚀 Features

- Disease prediction using symptoms  
- Voice input support  
- Multilingual support  
- Emergency ambulance feature  
- Hospital information  
- User dashboard  

---

## 🛠 Tech Used

- Python (Django)
- HTML, CSS, JavaScript
- Machine Learning

---

## ⚙️ How to Run

1. Download the project
2. Open terminal

### 1. Install Dependencies
cd AI_MedAssist
pip install -r requirements.txt

### 2. Train ML Models
cd models
python model_training.py
cd ..

### 3. Setup Django
cd backend
python manage.py makemigrations users diagnosis ambulance hospitals
python manage.py migrate
python manage.py shell < seed_data.py

### 4. Run Server
python manage.py runserver
