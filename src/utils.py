import os
import sys
import pickle
import dill
from src.exception import CustomException
from src.logger import logging  # Importing your project's logger

def save_object(file_path, obj):
    """
    Saves a python object to a specific file path using dill/pickle.
    """
    try:
        logging.info(f"Entered the save_object method for path: {file_path}")
        
        dir_path = os.path.dirname(file_path)

        # Create directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"Directory ensured: {dir_path}")

        with open(file_path, "wb") as file_obj:
            # Using dill for better compatibility with custom classes/lambdas
            dill.dump(obj, file_obj)
            
        logging.info(f"Object saved successfully at: {file_path}")

    except Exception as e:
        logging.error(f"Error occurred in save_object: {str(e)}")
        raise CustomException(e, sys)