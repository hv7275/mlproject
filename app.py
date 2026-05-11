import os
from flask import Flask, request, render_template, redirect, url_for, session
import numpy as np
import pandas as pd
from dotenv import load_dotenv

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

load_dotenv()

application = Flask(__name__)
application.secret_key = os.getenv('FLASK_SECRET_KEY')

app = application

## Route for home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
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
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        # Round the result for better UI display
        final_result = round(results[0], 2)
        session['results'] = final_result

        return redirect(url_for('predict_datapoint'))

    results = session.pop('results', None)
    return render_template('home.html', results=results)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)