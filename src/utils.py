from datetime import datetime
import pandas as pd
from langchain_openai  import OpenAI
from dotenv import load_dotenv
import os
import pickle



load_dotenv() 
api_key = os.getenv('OPENAI_API_KEY')
print(api_key)
llm = OpenAI(temperature=0, api_key=api_key)

def createPredictionPrompt(data, churn, probability):
    data = pd.DataFrame([data], index=[0])
    #print(data['Age'])
    text = f"""
    You are an analysi in a Wealth Management firm. and your job is to analyze the customer data and provide churn analysis and steps to prevent churn
    Based on the available details of Wealth Management firm customer, Machine learning model predicted as {churn} (0 for not churn, 1 for churn) with probability of {probability} Analyze the customer details and produce analysis summary and the steps to prevent churn based on analysis and customer details
    Customer Details =  Age: {data['Age'][0]}, Gender: {data['Gender'][0]}, Total_Amount_invested: {data['AUM'][0]}, Previous_AUM: {data['Previous_AUM'][0]}, Months_since_last_activity: {data['Months_since_last_activity'][0]} (less than 5 Months since last active is considered good, customer will not churn.), Customer_rating_for_service: {data['Customer_rating_for_service'][0]}(Customer_rating_for_service above 7 is good, below 6 is bad), Chat_Analysis_1: {data['Chat_Analysis_1'][0]}, Chat_Analysis_2: {data['Chat_Analysis_2'][0]}, Chat_Analysis_3: {data['Chat_Analysis_3'][0]}, Chat_Analysis_4: {data['Chat_Analysis_4'][0]}, Chat_Analysis_5: {data['Chat_Analysis_5'][0]}, Total_Returns_percentage: {data['Total_Returns_percentage_in_CAGR'][0]}, Last_1_year_returns_percentage: {data['Last_1_year_returns_percentage'][0]}, Total_Number_of_Complaints_Raised_Last_Year: {data['Total_Number_of_Complaints_Raised'][0]}, Number_of_Unresolved_Issues: {data['Number_of_Unresolved_Issues'][0]}, Net_Promoter_Score: {data['Net_Promoter_Score'][0]} (range 1 to 10), Customer_Category: {data['Category'][0]} For UHNW customer, Unacceptable if latest chat analysis is negative if it is Neutral then it is good, Unacceptable if more than 2 complaints were raised last year, Unacceptable if there is 1 unresolved issue. Weightage: 3 times. For HNW customer, Unacceptable if latest 2 chat analyses are negative, Unacceptable if more than 3 complaints were raised last year, Unacceptable if there are 2 unresolved issues.Weightage: 2 times. For MA customers, Unacceptable if latest 3 chat analyses are negative, Unacceptable if more than 5 complaints were raised last year, Unacceptable if there are 5 unresolved issues, Weightage: 1 time. Average good Customer_rating_for_service is 7. 
    Result should always be in below format.
	Analysis: 'Based on the provided customer details analyze and identify any potential risks, concerns, or patterns that require attention and reason why customer may churn or not churn(be specific for each customer and mention relevant data, don't provide generic statements) in one paragraph(less than 100 words)'
    Preventive Steps: 'Based on the analysis, provide clear and actionable prevention steps to address the identified issues or mitigate potential risks for this specific customer (don't provide generic statements, be specific for each customer) in one paragraph'
    """
    return text

def getCRMData():
    df = pd.read_csv('Data/train1.csv')

    df['Last_active_date'] = pd.to_datetime(df['Last_active_date'])
    today = datetime.today()
    df['Months_since_last_activity'] = (today - df['Last_active_date']) // pd.Timedelta(days=30)
    df = df.drop(columns=['Last_active_date'])
    return df



def predictChurn(data, llm=llm):
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    llm = OpenAI(temperature=0, api_key=api_key)
    pred = llm.predict(data)
    print(pred)
    return pred

def sentimentAnalysis(data, llm=llm):
    text = f"""
    Analyze and predict the sentiment of the Customer from the following convesation of Customer with Assistant.
    Text: {data}
    Output should always in below format
    Sentiment: 'sentiment (Positive / Neutral / Negative)'
    Analysis: 'Based on the provided conversation between customer and assistant, analyze the dialogue and extract the reason for the customer's call or the issue the customer is facing. Identify key phrases, keywords, or cues that indicate the purpose of the customer's contact or any problems they are encountering in small one line paragraph with less than 30 words'
    """
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    print(api_key+ '--------------------------')
    llm = OpenAI(name='gpt-3.5-turbo-0125', temperature=0, api_key=api_key)
    pred = llm.predict(text)
    pred = pred.split('Sentiment: ')[1]
    tmp = pred.split('Analysis: ')
    sentiment = tmp[0].replace('\n', '')
    analysis = tmp[1].replace('\n', '')
    print(analysis)
    
    return (sentiment, analysis)

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise Exception(e)
    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        print(f'Exception Occured in load_object function utils, ERROR {e}')
