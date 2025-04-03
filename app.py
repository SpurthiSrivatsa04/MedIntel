import os
import logging
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from utils.predict import symptoms_list, predict_disease

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///medicalmindai.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Prediction
from forms import LoginForm, RegistrationForm


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if username already exists
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('register.html', form=form)

            # Check if email already exists
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('register.html', form=form)

            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Successfully registered user: {user.username}")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')
        if symptoms:
            try:
                disease, confidence, details = predict_disease(symptoms)
                prediction = Prediction(
                    user_id=current_user.id,
                    symptoms=','.join(symptoms),
                    predicted_disease=disease,
                    confidence=confidence
                )
                db.session.add(prediction)
                db.session.commit()
                return render_template('predict.html',
                                    prediction=prediction,
                                    symptoms_list=symptoms_list,
                                    disease_details=details)
            except Exception as e:
                logger.error(f"Error during prediction: {str(e)}")
                flash('An error occurred during prediction. Please try again.', 'error')
                return render_template('predict.html', symptoms_list=symptoms_list)
        else:
            flash('Please select at least one symptom.', 'warning')
    return render_template('predict.html', symptoms_list=symptoms_list)

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's prediction history
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
                                .order_by(Prediction.timestamp.desc())\
                                .all()

    # Prepare data for visualizations
    diseases = {}
    symptoms_freq = {}
    timeline_data = []

    for pred in predictions:
        # Count disease occurrences
        diseases[pred.predicted_disease] = diseases.get(pred.predicted_disease, 0) + 1

        # Count symptom frequencies
        for symptom in pred.symptoms.split(','):
            symptoms_freq[symptom] = symptoms_freq.get(symptom, 0) + 1

        # Timeline data
        timeline_data.append({
            'date': pred.timestamp.strftime('%Y-%m-%d'),
            'disease': pred.predicted_disease,
            'confidence': pred.confidence
        })

    return render_template('dashboard.html',
                         predictions=predictions,
                         diseases=diseases,
                         symptoms_freq=symptoms_freq,
                         timeline_data=timeline_data)

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")