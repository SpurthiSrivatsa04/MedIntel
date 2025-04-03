import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_prescription(disease):
    """Generate prescription and dosage information based on the disease"""
    prescriptions = {
        "Drug Reaction": {
            "medications": [
                {"name": "Antihistamine (Diphenhydramine)", "dosage": "25-50mg", "duration": "Every 4-6 hours"},
                {"name": "Topical Corticosteroid", "dosage": "Apply thin layer", "duration": "2-3 times daily"}
            ],
            "notes": "Stop taking suspected drug immediately. Seek immediate medical attention if symptoms worsen."
        },
        "GERD": {
            "medications": [
                {"name": "Omeprazole", "dosage": "20mg", "duration": "Once daily before breakfast"},
                {"name": "Antacid", "dosage": "10-20ml", "duration": "As needed for breakthrough symptoms"},
                {"name": "Sucralfate", "dosage": "1g", "duration": "Four times daily, before meals"}
            ],
            "notes": "Take on empty stomach. Avoid lying down for 2 hours after meals. Elevate head of bed."
        },
        "Chronic cholestasis": {
            "medications": [
                {"name": "Ursodeoxycholic acid", "dosage": "13-15mg/kg", "duration": "Daily in divided doses"},
                {"name": "Vitamin D supplement", "dosage": "2000-4000 IU", "duration": "Daily"},
                {"name": "Vitamin K", "dosage": "5-10mg", "duration": "Weekly"}
            ],
            "notes": "Regular liver function monitoring required. Maintain adequate hydration."
        },
        "Peptic ulcer diseae": {
            "medications": [
                {"name": "Pantoprazole", "dosage": "40mg", "duration": "Once daily before breakfast"},
                {"name": "Sucralfate", "dosage": "1g", "duration": "Four times daily"},
                {"name": "Bismuth subsalicylate", "dosage": "525mg", "duration": "Four times daily"}
            ],
            "notes": "Avoid NSAIDs, alcohol, and spicy foods. Take medications regularly."
        },
        "Diabetes": {
            "medications": [
                {"name": "Metformin", "dosage": "500mg", "duration": "Twice daily with meals"},
                {"name": "Blood Glucose Monitoring", "dosage": "Check levels", "duration": "2-4 times daily"},
                {"name": "Regular Exercise", "dosage": "30 minutes", "duration": "Most days of the week"}
            ],
            "notes": "Monitor blood sugar regularly. Follow diabetic diet plan. Keep emergency glucose available."
        },
        "Gastroenteritis": {
            "medications": [
                {"name": "Oral Rehydration Solution", "dosage": "200-400ml", "duration": "After each loose stool"},
                {"name": "Probiotics", "dosage": "As per package", "duration": "Daily"},
                {"name": "Loperamide (if needed)", "dosage": "4mg initially, then 2mg", "duration": "After each loose stool"}
            ],
            "notes": "Stay hydrated. Avoid dairy and fatty foods initially. Seek medical attention if symptoms worsen."
        },
        "Bronchial Asthma": {
            "medications": [
                {"name": "Albuterol Inhaler", "dosage": "1-2 puffs", "duration": "Every 4-6 hours as needed"},
                {"name": "Corticosteroid Inhaler", "dosage": "2 puffs", "duration": "Twice daily"},
                {"name": "Peak Flow Monitoring", "dosage": "Check readings", "duration": "2-3 times daily"}
            ],
            "notes": "Keep rescue inhaler nearby. Follow asthma action plan. Avoid triggers."
        },
        "Hypertension": {
            "medications": [
                {"name": "Amlodipine", "dosage": "5-10mg", "duration": "Once daily"},
                {"name": "Regular BP Monitoring", "dosage": "Check BP", "duration": "Twice daily"},
                {"name": "Low-sodium diet", "dosage": "Less than 2300mg sodium", "duration": "Daily"}
            ],
            "notes": "Monitor blood pressure regularly. Reduce salt intake. Regular exercise recommended."
        },
        "Malaria": {
            "medications": [
                {"name": "Artemether/Lumefantrine", "dosage": "4 tablets", "duration": "Twice daily for 3 days"},
                {"name": "Paracetamol", "dosage": "500-1000mg", "duration": "Every 4-6 hours for fever"}
            ],
            "notes": "Complete full course of medication. Take artemether with food."
        },
        "Allergy": {
            "medications": [
                {"name": "Cetirizine", "dosage": "10mg", "duration": "Once daily"},
                {"name": "Calamine Lotion", "dosage": "Apply to affected area", "duration": "3-4 times daily"}
            ],
            "notes": "Avoid known allergens. Keep affected area clean and dry."
        },
        "Migraine": {
            "medications": [
                {"name": "Sumatriptan", "dosage": "50-100mg", "duration": "At onset, repeat after 2h if needed"},
                {"name": "Ibuprofen", "dosage": "400-800mg", "duration": "With first symptoms"}
            ],
            "notes": "Take at first sign of migraine. Rest in dark, quiet room."
        },
        "Hepatitis B": {
            "medications": [
                {"name": "Entecavir", "dosage": "0.5-1mg", "duration": "Once daily"},
                {"name": "Regular monitoring", "dosage": "Blood tests", "duration": "Every 3-6 months"}
            ],
            "notes": "Avoid alcohol completely. Regular liver function monitoring required."
        },
        "Common Cold": {
            "medications": [
                {"name": "Acetaminophen", "dosage": "500-1000mg", "duration": "Every 4-6 hours as needed"},
                {"name": "Decongestant", "dosage": "As per package", "duration": "3-5 days maximum"}
            ],
            "notes": "Stay hydrated. Rest. Use humidifier if available."
        },
        "Acute Liver Failure": {
            "medications": [
                {"name": "N-acetylcysteine", "dosage": "150mg/kg loading dose, then 70mg/kg every 4 hours", "duration": "Until liver function improves"},
                {"name": "Lactulose", "dosage": "30-45ml every 4-6 hours", "duration": "As needed to control encephalopathy"}

            ],
            "notes": "Close monitoring of liver function and blood ammonia levels is crucial.  May require ICU admission."
        },
        "Abnormal Menstruation": {
            "medications": [
                {"name": "Tranexamic acid", "dosage": "1000mg every 8-12 hours", "duration": "For 5 days"},
                {"name": "Combined oral contraceptive pill", "dosage": "As prescribed by physician", "duration": "Ongoing"}
            ],
            "notes": "This is a symptom and not a disease. Underlying conditions must be ruled out. Consult your doctor."
        }
    }

    # Default prescription for diseases not in the list
    default_prescription = {
        "medications": [
            {"name": "This condition requires professional medical evaluation",
             "dosage": "Please consult a healthcare provider",
             "duration": "As soon as possible"},
            {"name": "Self-monitoring",
             "dosage": "Monitor symptoms",
             "duration": "Until medical consultation"}
        ],
        "notes": "⚠️ This is a preliminary assessment only. The suggested condition requires proper medical diagnosis and treatment. Please consult a healthcare professional immediately for proper evaluation and care."
    }

    prescription = prescriptions.get(disease, default_prescription)
    prescription["disclaimer"] = "⚠️ This is an AI-generated suggestion and should not replace professional medical advice. Always consult a healthcare provider before starting any medication."

    return prescription

def load_disease_data():
    """Load and process disease and symptom data from CSV files"""
    try:
        # Use absolute paths based on the current directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        disease_path = os.path.join(base_dir, 'dataset_folder', 'DiseaseAndSymptoms.csv')
        precautions_path = os.path.join(base_dir, 'dataset_folder', 'Disease precaution.csv')

        # Load disease and symptoms data
        disease_df = pd.read_csv(disease_path)
        precautions_df = pd.read_csv(precautions_path)

        # Extract unique symptoms from all symptom columns
        symptom_columns = [col for col in disease_df.columns if col.startswith('Symptom_')]
        symptoms_set = set()
        for col in symptom_columns:
            symptoms_set.update(disease_df[col].dropna().unique())

        # Clean symptom strings
        symptoms_list = sorted([
            symptom.strip().lower().replace(' ', '_')
            for symptom in symptoms_set
            if isinstance(symptom, str)
        ])

        # Create disease-symptoms mapping
        disease_symptoms = {}
        for _, row in disease_df.iterrows():
            disease = row['Disease']
            symptoms = [
                str(row[col]).strip().lower().replace(' ', '_')
                for col in symptom_columns
                if pd.notna(row[col])
            ]
            if disease not in disease_symptoms:
                disease_symptoms[disease] = list(set(symptoms))  # Remove duplicates

        # Create disease information dictionary with precautions
        disease_info = {}
        for _, row in precautions_df.iterrows():
            disease = row['Disease']
            precautions = [
                p for p in [row.get(f'Precaution_{i}', '') for i in range(1, 5)]
                if pd.notna(p) and p != ''
            ]

            disease_info[disease] = {
                "description": "A medical condition requiring professional attention",
                "severity": "Varies",
                "duration": "Depends on treatment and severity",
                "recommendations": precautions,
                "prescription": get_prescription(disease)
            }

        logger.info(f"Loaded {len(symptoms_list)} symptoms and {len(disease_symptoms)} diseases")
        return symptoms_list, disease_symptoms, disease_info

    except Exception as e:
        logger.error(f"Error loading disease data: {str(e)}")
        raise

# Load data
symptoms_list, disease_symptoms, disease_info = load_disease_data()

# Prepare training data
X_train = []
y_train = []

for disease, symptoms in disease_symptoms.items():
    x = [1 if symptom in symptoms else 0 for symptom in symptoms_list]
    X_train.append(x)
    y_train.append(disease)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Train Naïve Bayes model
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

def predict_disease(selected_symptoms):
    """
    Predict disease based on selected symptoms using Naïve Bayes model.
    Returns disease name, confidence score, and detailed information.
    """
    try:
        if not selected_symptoms:
            return "Please select some symptoms", 0.0, None

        # Clean and standardize input symptoms
        selected_symptoms = [s.strip().lower().replace(' ', '_') for s in selected_symptoms]

        # Prepare input
        x_input = np.array([[1 if symptom in selected_symptoms else 0 for symptom in symptoms_list]])

        # Make prediction
        predicted_disease = nb_model.predict(x_input)[0]
        confidence = max(nb_model.predict_proba(x_input)[0]) * 100

        # Get disease details
        details = disease_info.get(predicted_disease, {
            "description": "Detailed information not available",
            "duration": "Varies",
            "severity": "Unknown",
            "recommendations": ["Consult a healthcare provider"],
            "prescription": get_prescription(predicted_disease)
        })

        logger.debug(f"Prediction: {predicted_disease} with {confidence:.2f}% confidence")
        return predicted_disease, confidence, details

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise