import os
import sqlite3
from functools import wraps

from flask import Flask, request, render_template, redirect, url_for, session, flash
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

from sklearn.preprocessing import StandardScaler
from models import create_user, get_user_by_identifier, init_db
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

load_dotenv()

application = Flask(__name__)
application.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

app = application


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'error')
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return wrapped_view


@app.before_request
def ensure_database():
    init_db()


## Route for home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password or not confirm_password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')

        password_hash = generate_password_hash(password)

        try:
            create_user(username, email, password_hash)
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')
            return render_template('register.html')

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')

        if not identifier or not password:
            flash('Username/email and password are required.', 'error')
            return render_template('login.html')

        user = get_user_by_identifier(identifier)

        if user is None or not check_password_hash(user['password_hash'], password):
            flash('Invalid username/email or password.', 'error')
            return render_template('login.html')

        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('Logged in successfully.', 'success')
        return redirect(url_for('predict_datapoint'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/predictdata', methods=['GET', 'POST'])
@login_required
def predict_datapoint():
    if request.method == 'POST':
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )

        pred_df = data.get_data_as_DataFrame()

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        # Round the result for better UI display
        final_result = round(results[0], 2)
        session['results'] = final_result

        return redirect(url_for('predict_datapoint'))

    results = session.pop('results', None)
    return render_template('home.html', results=results)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
