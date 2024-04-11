import pandas as pd
from datetime import datetime

from src.Customer import Customer
from src.utils import createPredictionPrompt, predictChurn
from src.utils import load_object
from src.predict_pipeline import predict_pipeline

class RelationshipManager:
    def __init__(self, id:int) -> None:
        self.df = pd.read_csv('Data/test.csv')
        self.pipeline = predict_pipeline()
        self.id = id
    
    def get_customers(self):
        df = pd.read_csv('Data/RM_Customer.csv')
        df = df[df['RM_ID'] == self.id]
        return df['customer_id'].to_list()
    
    def createData(self, customer_id):
        try:
            df = self.df
            df = df[df['Customer_id'] == customer_id]
            df['Last_active_date'] = pd.to_datetime(df['Last_active_date'],format='%d-%M-%Y')
            today = datetime.today()
            df['Months_since_last_activity'] = (today - df['Last_active_date']) // pd.Timedelta(days=30)
            df = df.drop(columns=['Last_active_date'])
            
            sentiments_df = Customer(customer_id).get_latest_convo(5)
            available_sentiments = len(sentiments_df)
            for i in range(5):
                col_name = f'Chat_Analysis_{i+1}'
                if(i >= available_sentiments):
                    df[col_name] = ''
                else:
                    df[col_name] = sentiments_df.iloc[i]['Analysis'].strip().replace('\n', ' ') if (sentiments_df.iloc[i]['Analysis'] != None or pd.isna(sentiments_df.iloc[i]['Analysis'])) else '' 
            
            c_sentiment, c_analysis = Customer(customer_id).get_latest_service_feedback_Analysys()
            if(c_analysis is None):
                df['Customer_service_feedback_Analysis'] = ''
                
            else:
                df['Customer_service_feedback_Analysis'] = c_analysis.strip().replace('\n', ' ')
                
            return df
        except Exception as e:
            raise e
        
    
    def get_churn_report(self):
        try:
            with open("Data/churn_report.csv", "w") as f:
                    f.write(f"customer_id#churn#probability#analysis#preventive_steps\n")
            customers = self.get_customers()
            for customer_id in customers:
                data = self.createData(customer_id)
                data.drop(['Customer_id', 'Location'], axis=1, inplace=True)
                pipeline = self.pipeline
                res = pipeline.predict(data)
                print(res)
                if res[0][0]>res[0][1]:
                    churn = 0
                    probability = res[0][0]
                else:
                    churn = 1
                    probability = res[0][1]
                prompt = createPredictionPrompt(data.iloc[0], churn, probability)
                print(prompt)
                pred = predictChurn(data=prompt)
                #print(pred)
                '''tmp = str(pred).split('Prediction: ')            
                tmp = tmp[1].split('Probability: ')
                churn = tmp[0].replace('\n', '')
                tmp = tmp[1].split('Analysis: ')
                probability = tmp[0].replace('\n', '')
                tmp = tmp[1].split('Preventive Steps: ')
                reason = tmp[0].replace('\n', '')
                preventive_steps = tmp[1].replace('\n', '')
                '''
                tmp = str(pred).split('Analysis: ')
                tmp = tmp[1].split('Preventive Steps: ')
                analysis = tmp[0].replace('\n', '')
                preventive_steps = tmp[1].replace('\n', '')
                with open("Data/churn_report.csv", "a") as f:
                    f.write(f"{customer_id}#{churn}#{probability}#{analysis}#{preventive_steps}\n")
                with open("Data/churn_history_report.csv", "a") as f:
                    f.write(f"{customer_id}#{churn}#{probability}#{analysis}#{preventive_steps}\n")
                
            df = pd.read_csv('Data/churn_report.csv', sep='#')
            return df
        except Exception as e:
            raise e
            
    