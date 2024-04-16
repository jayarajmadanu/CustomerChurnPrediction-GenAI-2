import pandas as pd
from datetime import datetime
import time

from src.Customer import Customer
from src.utils import createPredictionPrompt, predictChurn
from src.utils import load_object
from src.predict_pipeline import predict_pipeline
from typing import Set

class RelationshipManager:
    def __init__(self, id:int) -> None:
        df1 = pd.read_csv('Data/Affluenza-Customers-Testing-Data.csv')
        df2 = pd.read_csv('Data/Affluenza_CRM.csv')
        df = pd.merge(df1, df2, on='Customer_id')
        df['Customer_rating_for_service']=df['Customer_rating_for_service'].fillna(df['Customer_rating_for_service'].median())
        df['Net_Promoter_Score']=df['Net_Promoter_Score'].fillna(df['Net_Promoter_Score'].median())
        self.df = df
        self.pipeline = predict_pipeline()
        self.id = id
    
    def get_customers(self):
        df = pd.read_csv('Data/RM_Customer.csv')
        df = df[df['RM_ID'] == self.id]
        print(df['customer_id'].unique())
        return df['customer_id'].unique()
    
    def createData(self, customer_id):
        try:
            df = self.df
            df = df[df['Customer_id'] == customer_id]
            df['Last_active_date'] = pd.to_datetime(df['Last_active_date'],format='%Y-%M-%d')
            today = datetime.today()
            df['Months_since_last_activity'] = (today - df['Last_active_date']) // pd.Timedelta(days=30)
            df = df.drop(columns=['Last_active_date'])
            
            sentiments_df = Customer(customer_id).get_latest_convo(5)
            available_sentiments = len(sentiments_df)
            for i in range(5):
                col_name = f'Chat_Analysis_{i+1}'
                if(i >= available_sentiments):
                    df[col_name] = 'Positive'
                else:
                    df[col_name] = sentiments_df.iloc[i]['Sentiment'].strip().replace('\n', ' ') if (sentiments_df.iloc[i]['Sentiment'] != None or pd.isna(sentiments_df.iloc[i]['Sentiment'])) else 'Positive' 
            
            """
            c_sentiment, c_analysis = Customer(customer_id).get_latest_service_feedback_Analysys()
            if(c_analysis is None):
                df['Customer_service_feedback_Analysis'] = 'Positive'
                
            else:
                df['Customer_service_feedback_Analysis'] = c_sentiment.strip().replace('\n', ' ')
            """    
            return df
        except Exception as e:
            raise e
        
    def createPromptData(self, customer_id):
        try:
            df = self.df
            df = df[df['Customer_id'] == customer_id]
            df['Last_active_date'] = pd.to_datetime(df['Last_active_date'],format='%Y-%M-%d')
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
            """
            c_sentiment, c_analysis = Customer(customer_id).get_latest_service_feedback_Analysys()
            if(c_analysis is None):
                df['Customer_service_feedback_Analysis'] = ''
                
            else:
                df['Customer_service_feedback_Analysis'] = c_sentiment.strip().replace('\n', ' ')
            """    
            return df
        except Exception as e:
            raise e
    
    def get_churn_report(self):
        try:
            with open("Data/churn_report.csv", "w") as f:
                f.write(f"customer_id#churn#probability#analysis#preventive_steps\n")
            customers = self.get_customers()
            uniSet = set(customers)
            for customer_id in uniSet:
                time.sleep(1)
                print(customer_id)
                data = self.createData(customer_id)
                data.drop(['Customer_id', 'Name'], axis=1, inplace=True)
                pipeline = self.pipeline
                res = pipeline.predict(data)
                print(res)
                if res[0][0]>res[0][1]:
                    churn = 0
                else:
                    churn = 1
                probability = res[0][1]
                data = self.createPromptData(customer_id)
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
                with open("Data/churn_history_report.csv", "a") as fA:
                    fA.write(f"{customer_id}#{churn}#{probability}#{analysis}#{preventive_steps}\n")
                
            df = pd.read_csv('Data/churn_report.csv', sep='#')
            return df
        except Exception as e:
            raise e
            
    