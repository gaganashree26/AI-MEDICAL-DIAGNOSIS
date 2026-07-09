
import os
import sys

# Add backend to sys.path
sys.path.append(r'd:\AI_MedAssist\backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from ml_model.prediction_service import PredictionService

try:
    print("Attempting to initialize PredictionService...")
    service = PredictionService()
    print("Success!")
    print(f"Symptom list length: {len(service.get_symptom_list())}")
    
    test_symptoms = ['fever', 'cough']
    print(f"Attempting prediction for {test_symptoms}...")
    result = service.predict(test_symptoms)
    print(f"Result: {result['predicted_disease']} ({result['confidence_score']}%)")
    
except Exception as e:
    print(f"Error occurred: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
