import os
import sys
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifact', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self, train_array, test_array, preprocessor_path):
        try:
            logging.info('Spliting Training And Test Input Data')
            
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            ) 
            
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(
                    verbose=False, 
                    allow_writing_files=False
                ),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'max_depth': [5, 10, 15, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                "Random Forest": {
                    'n_estimators': [64, 128, 256],
                    'max_depth': [10, 20, None],
                    'min_samples_split': [2, 5],
                    'max_features': ['sqrt', 'log2', None]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.05, 0.01],
                    'n_estimators': [100, 200],
                    'subsample': [0.8, 0.9, 1.0],
                    'max_depth': [3, 5, 8]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [0.1, 0.01, 0.05],
                    'n_estimators': [100, 200],
                    'max_depth': [5, 7, 10],
                    'lambda': [1, 0.5] # L2 regularization
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [100, 200]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [0.1, 0.5, 1.0],
                    'n_estimators': [50, 100, 200],
                    'loss': ['linear', 'square', 'exponential']
                }
            }
            
            model_report:dict=evaluate_models(
                X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                models=models,param=params
            )
            
            ## To get best model score from dict
            best_model_score = max(model_report.values())
            
            ## To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found with R2 score above 0.6")

            logging.info(f"Best model found: {best_model_name} with R2: {best_model_score}")
            
            # Note: Best model is already fitted inside evaluate_models (GridSearchCV)
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square

        except Exception as e:
            logging.error(f"Error occurred in Model Training: {str(e)}")
            raise CustomException(e, sys)