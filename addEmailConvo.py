import pandas as pd
from datetime import datetime

from src.Customer import Customer

email_df = pd.read_excel('Data/raw/Affluenza Customer Communications-Emails.xlsx')

print('Adding Email convo')
for idx, row in email_df.iterrows():
    cust = Customer(row['Customer_id'], 'Add Email')
    #date = datetime.strptime(row['Date'], '%d-%M-%Y')
    cust.add_email_convo(row['conversation'], row['Date'])
    
print('Added Email convo')
    