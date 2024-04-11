import pandas as pd
import uuid
from datetime import datetime

from src.utils import sentimentAnalysis

class Customer:
    def __init__(self, id:int) -> None:
        df_chat = pd.read_csv("Data/chat_convo.csv", sep='#')
        df_email = pd.read_csv("Data/email_convo.csv", sep='#')
        df_chat["date"] = pd.to_datetime(df_chat["date"])
        df_email["date"] = pd.to_datetime(df_email["date"])
        self.df = pd.concat([df_chat, df_email])
        self.feed_df = pd.read_csv("Data/feedback.csv", sep='#')
        self.id = id
        
    def get_latest_convo(self, no_of_convos:int):
        df = self.df[self.df["customer_id"] == self.id].sort_values(by="date", ascending=False).head(no_of_convos)
        return df
    
    def add_chat_convo(self, message:str):
        date = datetime.now()
        sentiment, analysis = sentimentAnalysis(message)
        sentiment = sentiment.replace("\n", " ")
        analysis = analysis.replace("\n", " ")
        record = f"{uuid.uuid4()}#{self.id}#{message}#{date}#{sentiment}#{analysis}"
        record = record.replace("\n", " ")
        record = f"\n{record}"
        
        with open("Data/chat_convo.csv", "a") as f:
            f.write(record)
    
    def add_email_convo(self, message:str):
        date = datetime.now()
        sentiment, analysis = sentimentAnalysis(message)
        sentiment = sentiment.replace("\n", " ")
        analysis = analysis.replace("\n", " ")
        record = f"{uuid.uuid4()}#{self.id}#{message}#{date}#{sentiment}#{analysis}"
        record = record.replace("\n", " ")
        record = f"\n{record}"
        with open("Data/email_convo.csv", "a") as f:
            f.write(record)
            
    def add_customer_feedback(self,feedback:str):
        date = datetime.now()
        sentiment, analysis = sentimentAnalysis(feedback)
        record = f"{uuid.uuid4()}#{self.id}#{feedback}#{date}#{sentiment}#{analysis}"
        record = record.replace("\n", " ")
        record = f"\n{record}"
        with open("Data/feedback.csv", "a") as f:
            f.write(record)
            
    def get_latest_service_feedback_Analysys(self):
        df = self.feed_df[self.feed_df["customer_id"] == self.id].sort_values(by="date", ascending=False).reset_index(drop=True)
        if(len(df) == 0):
            return (None, None)
        return (df.iloc[0]["Sentiment"], df.iloc[0]["Analysis"])
        

        
        