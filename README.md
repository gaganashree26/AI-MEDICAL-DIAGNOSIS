# AI Based Medical Diagnosis Assistant Using Machine Learning

An AI-powered healthcare web application that predicts diseases based on symptoms using Machine Learning models (Random Forest + XGBoost ensemble).

## Features

- **Disease Prediction** - ML models predict diseases from symptoms with 98%+ accuracy
- **Confidence Score** - Every diagnosis includes a transparency/reliability rating
- **International Support** - Designed for global accessibility in English
- **Manual & Voice Input** - Hands-free symptom entry or intuitive manual typing
- **Emergency Ambulance** - One-click ambulance dispatch
- **Dashboard** - Diagnosis history, health analytics, and profile management
- **Rural Healthcare** - Optimized for low-bandwidth environments
- **JWT Authentication** - Secure user registration and login

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, Django, Django REST Framework |
| Database | SQLite |
| ML Models | Scikit-learn, XGBoost, Pandas, NumPy |
| Auth | JWT (SimpleJWT) |

## Quick Start

### 1. Install Dependencies
```bash
cd AI_MedAssist
pip install -r requirements.txt
```

### 2. Train ML Models
```bash
cd models
python model_training.py
cd ..
```

### 3. Setup Django
```bash
cd backend
python manage.py makemigrations users diagnosis ambulance hospitals
python manage.py migrate
python manage.py shell < seed_data.py
```

### 4. Run Server
```bash
python manage.py runserver
```

### 5. Access Application
- **Home**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Admin**: http://127.0.0.1:8000/admin/

### Default Credentials
- **Admin**: admin / your_secure_admin_password
- **Demo User**: demo / your_secure_demo_password

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register/ | User registration |
| POST | /api/login/ | User login (JWT) |
| POST | /api/predict/ | Disease prediction |
| GET | /api/history/ | Diagnosis history |
| GET | /api/symptoms/ | Supported symptoms list |
| GET | /api/dashboard/ | Dashboard statistics |
| POST | /api/voice-input/ | Voice transcript processing |
| POST | /api/request-ambulance/ | Ambulance dispatch |
| GET | /api/hospitals/ | Nearby hospitals |
| GET | /api/profile/ | User profile |

## Project Structure

```
AI_MedAssist/
├── backend/
│   ├── manage.py
│   ├── seed_data.py
│   ├── config/          # Django settings & URLs
│   ├── users/           # Authentication & profiles
│   ├── diagnosis/       # Disease prediction & history
│   ├── ambulance/       # Emergency ambulance support
│   ├── hospitals/       # Hospital directory
│   ├── ml_model/        # ML prediction service
│   ├── voice/           # Voice input processing
│   └── multilingual/    # Translation service
├── frontend/
│   ├── index.html       # Landing page
│   ├── login.html       # Login
│   ├── register.html    # Registration
│   ├── diagnosis.html   # Symptom checker
│   ├── result.html      # Prediction results
│   ├── dashboard.html   # Clinical dashboard
│   ├── ambulance.html   # Emergency support
│   ├── about.html       # About project
│   ├── contact.html     # Contact page
│   ├── rural_healthcare.html
│   └── js/api.js        # API service module
├── models/
│   └── model_training.py
├── dataset/
│   └── disease_dataset.csv
├── requirements.txt
└── README.md
```

## License
This project is for educational purposes.
