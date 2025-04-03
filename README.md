# MedIntel - AI-Based Symptom Analyzer

MedIntel is an AI-powered disease prediction system that leverages Natural Language Processing (NLP) and Machine Learning (Naïve Bayes) to provide real-time symptom-based diagnosis. It features a Flask web app for user interaction and a Streamlit dashboard for data visualization.

## Features
- **Multi-Class Disease Prediction**: Uses Naïve Bayes classifier for conditions like diabetes and hypertension.
- **TF-IDF Feature Engineering**: Enhances precision by 15%.
- **Real-Time Symptom Analysis**: Flask-based web app for live predictions.
- **Flask Dashboard**: Visualizes symptom trends and treatment insights.
- **5-Fold Cross-Validation**: Achieves an AUC-ROC score of 0.89.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SpurthiSrivatsa04/MedIntel.git
   cd MedIntel
   ```
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the Flask Web App
```bash
flask run
```
- Open `http://127.0.0.1:5000/` in your browser.
- Enter symptoms to receive predictions.

## Project Structure
```
MedIntel/
│── app.py                   # Flask web app
│── main.py                  # Entry point
│── models.py                # ML models
│── forms.py                 # User input handling
│── utils/
│   ├── predict.py           # Prediction logic
│── static/
│   ├── css/style.css        # Stylesheets
│   ├── js/script.js         # JavaScript logic
│── templates/
│   ├── index.html           # Homepage
│   ├── predict.html         # Prediction UI
│   ├── dashboard.html       # Data visualization
│── requirements.txt         # Dependencies
│── README.md                # Documentation
```

## Contribution
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add new feature"`).
4. Push to GitHub (`git push origin feature-name`).
5. Open a pull request.

## License
This project is licensed under the Adobe  License.

