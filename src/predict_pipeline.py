import pickle

from src.utils import load_object
class predict_pipeline:
    def __init__(self):
        self.model = load_object("models/best_model.pkl")
        self.preprocessor1 = load_object("models/preprocessor1.pkl")
        self.preprocessor2 = load_object("models/preprocessor2.pkl")
        
    def predict(self, data):
        try:
            data = self.preprocessor1.transform(data)
            data = self.preprocessor2.transform(data)
            prediction = self.model.predict_proba(data)
            return prediction
        except Exception as e:
            raise e