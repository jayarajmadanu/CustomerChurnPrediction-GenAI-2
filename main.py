import pandas as pd
import streamlit as st
from streamlit_modal import Modal

from src.RelationshipManager import RelationshipManager
from src.utils import getCRMData, sentimentAnalysis
from src.Customer import Customer


#df = getCRMData()

#text = """
#Customer: i ordered some stockes but they didn't transfer into my account.
#Assistant: it will take 1 business day to transfer the money into my account.
#Customer: ok thankyou
#"""
#senti = sentimentAnalysis(llm, text)
#print(senti)
st.title("ChurnShield")
st.markdown("""
<style>
body {
  background: red; 
  background: -webkit-linear-gradient(to right, #ff0099, #493240); 
  background: linear-gradient(to right, #ff0099, #493240); 
}
</style>
    """, unsafe_allow_html=True)
st.session_state.open_modal = False
rm = None
#rm1.get_churn_report()
def get_report(rm):
    id = st.session_state['rm_id']
    rm = RelationshipManager(int(id))
    rm.get_churn_report()
    df = pd.read_csv('Data/churn_report.csv',sep='#')
    df.sort_values(by='probability', ascending=False, inplace=True)
    return df
st.session_state['rm_object'] = None

with st.form(key='RM Login'):
    id = st.text_input('RM ID')
    submit = st.form_submit_button('Login')
    
    if submit:
        st.write(f"Welcome {id}")       
        st.session_state['rm_id'] = id

        
report_button = st.button(label='Get Churn Report')
if report_button:
   
    if 'rm_id' not in st.session_state:
        st.write("Please Login First")
    else :
        df = get_report(rm)
        for index, row in df.iterrows():
            st.write(pd.DataFrame([row], index=[0]))
            customer_id = row['customer_id']
            modal = Modal(key=customer_id,title=f'{customer_id} Details')
            cust_details = st.button(label=f'Get {customer_id} Details')
            #if cust_details:
            #    id = st.session_state['rm_id']
            #    rm = RelationshipManager(int(id))
            #    #st.(rm.createData(customer_id))
            #    st.warning(rm.createData(customer_id), icon="⚠️")
        #st.write(get_report(rm))

