from flask import FLask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

application = FLask(__name__)

app = application


## route for home page
@app.route('/')
def index():
    return render_template('index.html')