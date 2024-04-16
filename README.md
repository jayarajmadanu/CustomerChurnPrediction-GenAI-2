# ChurnShield - GenAI Powered Customer Churn Prediction and Prevention

## Description
This project presents a predictive model tailored for wealth management firms to forecast customer churn, along with a comprehensive analysis and actionable steps to prevent churn. The model is designed to assist Relationship Managers (RMs) in identifying at-risk customers and implementing proactive strategies to retain them.


## Key Features
Churn Prediction & Probability: Utilizes a machine learning (ML) model to predict customer churn and estimate the probability of churn for individual clients.
Analysis and Preventive Steps: Employs a Generative AI (GenAI) model to analyze customer data and recommend strategic actions to mitigate churn risk.
RM Integration: Designed for seamless integration into the workflow of Relationship Managers, providing churn reports and actionable insights for their client portfolios.

Architecture

![Architecture Diagram](img/archiDiad.PNG)

* As, get-churn-report API call initiated, RM module will fetch the customers allocated to him/her
* For each customer, RM module will fetch customer details, CRM Data, Frontend communications(Emails, Chats, MOMs) and provide it to ML model for churn prediction
* The prediction results along with probability and customer data(details, CRM Data, Frontend communications) will be given as inputs to LLM to provide Customer Analysis and steps to recommend best actions to prevent churn
* LLM is being used to process Frontend communications, LLM model will provide sentiment analysis and text summarization for further processing
* For ML model sentiment analysis of Frontend communications will be used to predict churn
* For LLM, test summarization is used as input to provide analysis and preventive steps

## Installation
1. Clone the project into your local machine
```
git clone https://github.com/jayarajmadanu/CustomerChurnPrediction-GenAI-2.git
```
2. Create seperate conda environment(Optional)
```
conda create -p venv python=3.11.4
```
3. Install required packages from requirements.txt file
```
pip install -r requirements.txt
```

## Usage
ChurnShield Application provides 2 APIs 
1. To get the churn report of customers under RM(Method type: POST)
```
http://127.0.0.1:5000/get-churn-report
```
provide RM id in the body
```
{
    "rm_id":"2001"
}
```

2. To train the ML model with Data(Method Type: GET)
```
http://127.0.0.1:5000/train
```