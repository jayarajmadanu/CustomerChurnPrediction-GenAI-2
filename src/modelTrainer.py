from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, make_scorer, precision_score, f1_score
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from src.utils import save_object

class ModelTrainer:
    
    def evaluate_models(self, X_train,y_train, X_test,y_test, models:dict, params:dict):
        model_keys = models.keys()
        report = {}

        for model_name in model_keys:
            model = models[model_name]
            parameters = params[model_name]
            print(f"Training {model_name}")
            # GridSearchCV will get best hypermaters for each model
            custom_scorer = make_scorer(precision_score, greater_is_better=True,  pos_label=1)
            gs = GridSearchCV(estimator=model, param_grid=parameters, cv=3, scoring=custom_scorer)
            gs.fit(X_train, y_train)

            # now test the model with training data

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            y_test_pred = model.predict(X_test)
            print(f"Y_pred = {y_test_pred}")

            cm = confusion_matrix(y_test, y_test_pred)
            test_model_score = accuracy_score(y_test, y_test_pred)
            classifi_report = classification_report(y_true=y_test, y_pred=y_test_pred)
            with open("Reports/train_classification_report.txt", "a") as f:
                    f.write(f"\nConfusion Matrix for model {model_name} is \n {cm}")
                    f.write(f"\nClassification Report for model {model_name} is  \n {classifi_report}")
                    f.write(f"\nAccuracy score for {model_name} is {test_model_score}")
            print(f"Confusion Matrix for model {model_name} is \n {cm}")
            print(f"Classification Report for model {model_name} is  \n {classifi_report}")
            
            print(f"Accuracy score for {model_name} is {test_model_score}")

            y_train_pred = model.predict(X_train)
            train_model_score = f1_score(y_train, y_train_pred)
            report[model_name] = {
                'model' : model,
                'model_name': model_name,
                'f1_score_test' : test_model_score,
                'f1_score_train' : train_model_score,
                'best_params': gs.best_params_
            }
        print(f'Model Evaluation report: \n{report}')
        with open("Reports/train_report.txt", "a") as f:
            f.write(f'Model Evaluation report: \n{report}')
        return report
    
    def train_model(self):
        df = pd.read_csv('Data/final_transformed.csv')
        X = df.iloc[:, 0:17]
        y = df.iloc[:, 17].astype(int)
        
        X_train, X_test, y_train, y_test  = train_test_split(X,y, test_size=0.3, random_state=57)
        
        params = {
            "Random Forest": {
                "max_features": [
                "sqrt",
                "log2"
                ],
                "n_estimators": [
                8,
                16,
                32,
                64,
                128,
                256
                ],
                "max_depth": [
                7,
                9,
                11,
                13
                ],
                "n_jobs": [
                -1
                ],
            },
            "SVR": {

            },
            "Gradient Boosting": {
                "learning_rate": [
                0.1,
                0.01,
                0.05,
                0.001
                ],
                "subsample": [
                0.75,
                0.8,
                0.85,
                0.9
                ],
                "max_features": [
                "sqrt",
                "log2"
                ],
                "n_estimators": [
                128,
                256,
                512
                ],
                "max_depth": [
                3,
                5,
                6
                ]
            },
            "XGBClassifier": {
                "learning_rate": [
                0.05,
                0.08,
                0.1
                ],
                "n_estimators": [
                4,
                8,
                16,
                32,
                64,
                128,
                256
                ],
                "max_depth": [
                5,
                7,
                10,
                12
                ]
            },
            "AdaBoost Classifier": {
                "learning_rate": [
                0.1,
                0.01,
                0.05,
                0.2
                ],
                "n_estimators": [
                8,
                16,
                32,
                64,
                128,
                256
                ]
            }
            }

        models = {
            "Random Forest": RandomForestClassifier(),
            "XGBClassifier": XGBClassifier(),
            "AdaBoost Classifier": AdaBoostClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
        }           
        
        report = self.evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=params)
        
        best_model_name = ""
        max_f1_score_test = 0
        for model_name in report.keys():
            if max_f1_score_test < report[model_name]['f1_score_test']:
                max_f1_score_test = report[model_name]['f1_score_test']
                best_model_name = model_name

        best_model = report[best_model_name]['model']
         
        with open("Reports/best_model.txt", "a") as f:
            f.write(f'Best Model: \n{best_model}')
        save_object('models/best_model.pkl', best_model)
              