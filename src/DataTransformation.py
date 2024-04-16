import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from src.Customer import Customer
from src.utils import save_object

class DataTransformation:
    
    def dataset_creation(self):
        df1 = pd.read_csv('Data/Affluenza-Customers-Training-Data.csv')
        df2 = pd.read_csv('Data/Affluenza_CRM.csv')
        df = pd.merge(df1, df2, on='Customer_id')
        df['Last_active_date'] = pd.to_datetime(df['Last_active_date'],format='%Y-%M-%d')
        today = datetime.today()
        df['Months_since_last_activity'] = (today - df['Last_active_date']) // pd.Timedelta(days=30)
        df = df.drop(columns=['Last_active_date'])
        df['Customer_rating_for_service']=df['Customer_rating_for_service'].fillna(df['Customer_rating_for_service'].median())
        df['Net_Promoter_Score']=df['Net_Promoter_Score'].fillna(df['Net_Promoter_Score'].median())
        
        df_chat = pd.read_csv("Data/chat_convo.csv", sep='#')
        df_email = pd.read_csv("Data/email_convo.csv", sep='#')
        df_chat["date"] = pd.to_datetime(df_chat["date"])
        df_email["date"] = pd.to_datetime(df_email["date"])
        convo_df = pd.concat([df_chat, df_email])
        convo_df.head()
        
        #feed_df = pd.read_csv("Data/feedback.csv", sep='#')
        
        for i in range(df.shape[0]):
            #customer = Customer(int(df.iloc[i]['Customer_id']))
            sentiments_df = convo_df[convo_df["customer_id"] == int(df.iloc[i]['Customer_id'])].sort_values(by="date", ascending=False).head(5)
            available_sentiments = len(sentiments_df)
            for j in range(5):
                col_name = f'Chat_Analysis_{j+1}'
                if(j<available_sentiments):
                    print(f"{df.iloc[i]['Customer_id']}---{j} ---{sentiments_df.iloc[j]['Sentiment'] == None or pd.isna(sentiments_df.iloc[j]['Sentiment'])} ----{sentiments_df.iloc[j]['Sentiment']}")
                    if (sentiments_df.iloc[j]['Sentiment'] == None or pd.isna(sentiments_df.iloc[j]['Sentiment'])):
                        df.loc[i, col_name] = 'Positive'
                    else :
                        df.loc[i, col_name] =  sentiments_df.iloc[j]['Sentiment'].strip()
                else:
                    df.loc[i, col_name] = 'Positive'
            """
            customer_feedback = self.get_latest_service_feedback_Analysys(feed_df, df.iloc[i]['Customer_id'])
            if(customer_feedback is None):
                df.loc[i, 'Customer_service_feedback_Analysis'] = 'Positive'
            else:
                df.loc[i, 'Customer_service_feedback_Analysis'] = customer_feedback.strip()
            """
        df.to_csv('Data/final.csv',index=False)
        
        
    def data_transformation(self):
        df = pd.read_csv('Data/final.csv')
        df.drop(['Customer_id', 'Name'], axis=1, inplace=True)
        X = df.drop('Churn', axis=1)
        y = df['Churn']
        cats = [['Female','Male'],['MA','HNW','UHNW'],['Negative','Neutral','Positive'],['Negative','Neutral','Positive'],['Negative','Neutral','Positive'],['Negative','Neutral','Positive'],['Negative','Neutral','Positive']]
        cols = ['Gender', 'Category', 'Chat_Analysis_1', 'Chat_Analysis_2',
       'Chat_Analysis_3', 'Chat_Analysis_4', 'Chat_Analysis_5']
        
        preprocessor1 = ColumnTransformer(
            transformers=[
                ('OrdinalEncoder', Pipeline(steps=[('OrdinalEncoder', OrdinalEncoder(categories=cats, dtype=int))]), cols),
            ], remainder='passthrough')
        
        preprocessor2 = ColumnTransformer(
            transformers=[
                ('StandardScaler', Pipeline(steps=[('StandardScaler', StandardScaler())]), slice(0,19))
            ], remainder='passthrough')
        
        Xx = preprocessor1.fit_transform(X)
        print(Xx)
        X = preprocessor2.fit_transform(Xx)
        
        
        df = np.c_[X, y]
        df = pd.DataFrame(df)
        df.to_csv('Data/final_transformed.csv', index=False)
        
        save_object('models/preprocessor1.pkl', preprocessor1)
        save_object('models/preprocessor2.pkl', preprocessor2)
        
    
    def get_latest_service_feedback_Analysys(self, feed_df, id):
        df = feed_df[feed_df["customer_id"] == id]
        if(len(df) == 0):
            return None
        return df.iloc[0]["Sentiment"]