from flask import Flask, render_template, request
import os 
import json
import numpy as np
import pandas as pd
import logging
import socket

from src.RelationshipManager import RelationshipManager
from src.DataTransformation import DataTransformation
from src.modelTrainer import ModelTrainer


app = Flask(__name__) # initializing a flask app
socket.setdefaulttimeout(100)
@app.route('/get-churn-report',methods=['POST'])
def get_churn():
    rm_id = 0
    if request.method == 'POST':
        data = json.loads(request.data)
        rm_id = int(data['rm_id'])
        logging.info(f'Logger {rm_id}')
        print(rm_id)
    rm = RelationshipManager(rm_id)
    df = rm.get_churn_report()
    res = df.to_json(orient="split")
    return res

@app.route('/train',methods=['GET'])
def train_model():
    dataTransformation = DataTransformation()
    dataTransformation.dataset_creation()
    dataTransformation.data_transformation()
    
    modelTrainer = ModelTrainer()
    modelTrainer.train_model()
    
    return "Model Trained"
    
if __name__ == "__main__":
	app.run(host="0.0.0.0", port = 8080, debug=True)
	#app.run(host="0.0.0.0", port = 8080)