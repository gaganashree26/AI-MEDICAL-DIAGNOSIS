# 🧠 AI Medical Based Diagnosis Assistant Using Machine Learning

This is a smart healthcare web application that predicts diseases based on user symptoms using Machine Learning.

---

## 🚀 Features

* Disease prediction based on symptoms
* Voice input support
* Multilingual support
* Emergency ambulance feature
* Hospital information system
* User dashboard

---

## 🛠 Tech Stack

* Python (Django)
* HTML, CSS, JavaScript
* Machine Learning

---

## ⚙️ How to Run

### 1. Download the Project

```bash
git clone https://github.com/gaganashree26/AI-FAKE-REVIEW-DETECTOR.git
cd AI-FAKE-REVIEW-DETECTOR
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train Machine Learning Model

```bash
cd models
python model_training.py
cd ..
```

### 4. Setup Django Backend

```bash
cd backend
python manage.py makemigrations users diagnosis ambulance hospitals
python manage.py migrate
python manage.py shell < seed_data.py
```

### 5. Run the Server

```bash
python manage.py runserver
```

---

## 👩‍💻 Author

**Gaganashree P**
Project Repository: https://github.com/gaganashree26/AI-MEDICAL-DIAGNOSIS.git
