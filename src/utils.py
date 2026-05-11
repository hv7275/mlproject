import os
import sys
import pickle
from src.exception import CustomException
from src.logger import logging 

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            
        logging.info(f"Object saved successfully at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        # Iterate using .items() for cleaner access to names and model objects
        for model_name, model in models.items():
            para = param.get(model_name, {})

            logging.info(f"Starting Hyperparameter tuning for: {model_name}")
            
            # GridSearchCV handles cross-validation and finding the best params
            gs = GridSearchCV(model, para, cv=3, n_jobs=-1, verbose=1)
            gs.fit(X_train, y_train)

            # Update model with the best parameters found
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # Evaluate on the test set
            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score
            logging.info(f"Model: {model_name} | R2 Score: {test_model_score}")

        return report

    except Exception as e:
        logging.error(f"Error occurred in evaluate_models: {str(e)}")
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
            
        with open(file_path, "rb") as file_obj:
            logging.info(f'Successfully loaded file: {file_path}')
            return pickle.load(file_obj)

    except Exception as e:
        logging.error(f'Error occurred on loading pickle file {file_path}')
        raise CustomException(e, sys)