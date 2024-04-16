import pandas as pd
import time
from dotenv import load_dotenv

from src.Customer import Customer
import os


load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print(key)
chat_df = pd.read_excel('Data/raw/Affluenza Customer Communications-Chats.xlsx')

print('Adding Chat convo')
for idx, row in chat_df.iterrows():
    cust = Customer(row['Customer_id'], 'Add Email')
    #date = datetime.strptime(row['Date'], '%d-%M-%Y')
    #d = row['Date'].split('-')
    #x = datetime(int(d[2]), int(d[1]), int(d[0]))
    #con = row['conversation'].split(' ')
    #if len(con) >150:
    #    con = con[:150]
    cust.add_chat_convo(row['conversation'], row['Date'])
    time.sleep(2)
    
print('Added Chat convo')
    