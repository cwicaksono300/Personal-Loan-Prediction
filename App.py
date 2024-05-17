import streamlit as st
import pandas as pd
import numpy as np
import pickle

#Configration Page
st.set_page_config("Personal Loan Prediction",page_icon=':dollar:',layout='wide')
style = "<style>h2 {text-align: center};color=Red"
st.markdown(style,unsafe_allow_html=True)

if 'submited' not in st.session_state:
    st.session_state['submited'] = False
if 'predicted' not in st.session_state:
    st.session_state['predicted'] = False
def submit_button():
    st.session_state.submited = True
def cancel_button():
    st.session_state.submited = False
def predict_button():
    st.session_state['predicted'] = True

#Function
def load_model():
    with open('RFClassifier.sav','rb') as file:
        model = pickle.load(file)
    return model

def predict(data:pd.DataFrame):
    model = load_model()
    prob = model.predict_proba(data)
    return prob[:,1]


#Title and Note
st.title("Personal Loan Prediction")
st.write("""
Welcome to the Personal Loan Campaign Prediction Tool. 
This application helps banks and financial institutions determine the likelihood of customers accepting personal loan offers.
Simply input the customer details below and get instant predictions.
"""
)
st.divider()

with st.sidebar:
    st.header("Menu",divider='gray')
    st.button("Home",use_container_width=True)
    st.button('Setting',use_container_width=True)
    st.button("About",use_container_width=True)


#Main Pages
#Membuat dua kolom
left_panel,right_panel = st.columns(2, gap='medium')
#Left Panel
left_panel.header('Information Panel')
#Membuat Tabs Overviews di left Panel
tabs1,tabs2 = left_panel.tabs(['Overview','Challenge'])
#Tabs1
tabs1.subheader('Overview')
tabs1.write("""
In the financial industry, particularly within banking, personal loan offerings are a critical product line that can significantly impact customer satisfaction and bank profitability. The challenge is not just to offer loans, but to ensure that they are targeted to the right customers who are most likely to accept the loan while also being capable of repaying it without defaulting.
""")

#Tabs2
tabs2.subheader('Challenge')
tabs2.write("""
Financial institutions often face challenges in identifying the right customer segments that would benefit from personal loan offers. Traditional approaches may lead to ineffective targeting, resulting in low conversion rates and high marketing costs. Objective: Develop a predictive model that can identify potential customers who are not only likely to accept a personal loan offer but are also likely to repay it successfully. This model will help in optimizing marketing strategies by focusing efforts and resources on the most promising leads.
""")

#Right Panel
right_panel.header('Prediction')
placeholder = right_panel.empty()
input_container = placeholder.container()

cust_id = input_container.text_input('Customer ID :', label_visibility='collapsed',placeholder='Customer ID :')
input_container.write("\n")
input_left, input_right = input_container.columns(2)

#Feature Left
input_left.write("**Personal Information**")
age = input_left.number_input('Age', min_value=17, max_value=75,step=1)
education = input_left.selectbox("Education", options=["Undergraduate","Graduate","Advance/Profesional"])
income = input_left.number_input('Annual Income (in thousand)',step=10)
family = input_left.number_input('Family Size', min_value=1,max_value=50,step=1)
experience = input_left.number_input('Profesional Experience', step=1)
house = input_left.number_input('Mortage Value of House (in Thousand)',step=10)

#Feature Right
input_right.write("**Bank Account Information**")
ccavg = input_right.number_input('Monthly Credit Card Spending ($ thousand)',step=10)
ccd = input_right.selectbox('Have Credit Card Account',options=['Yes','No'])
cda = input_right.selectbox('Have Certificate Deposit Account',options=['Yes','No'])
security = input_right.selectbox('Have Security Account',options=['Yes','No'])
online = input_right.selectbox('Using Internet Banking',options=['Yes','No'])

#Mapping
education_map = {"Undergraduate":1,"Graduate":2,"Advance/Profesional":3}
education = education_map[education]
bool_map = {'Yes':1,'No':2}
ccd = bool_map[ccd]
cda = bool_map[cda]
security = bool_map[security]
online = bool_map[online]

data = {"Personal Information":["Customer ID",'Age',"Annual Income","Family Size",'Profesional Experience','Mortage House Value','Monthly Credit Card Spending ($ thousand)','Have Credit Card Account','Have Certificate Deposit Account','Have Security Account','Using Internet Banking'],"Value":[cust_id,age,income, family, experience,house, ccavg, ccd,cda,security,online]}

#Submit Button
input_container.divider()
btn_submit = input_container.button('Submit',use_container_width=True, on_click=submit_button)

if st.session_state['submited']:
    placeholder.dataframe(data, use_container_width=True)
    right_panel.divider()
    btn_cancel = right_panel.button('Cancel',use_container_width=True,on_click=cancel_button)
    btn_predict = right_panel.button('Predict',use_container_width=True,on_click=predict_button,disabled=st.session_state.get("predicted", True))
    if btn_predict:
        data = {'Age':age,"Income":income,"Family":family,'Experience':experience,'Mortgage':house,'CCAvg':ccavg,'CreditCard':ccd,'CD Account':cda,'Securities Account':security,'Online':online,'Education':education}
        data = pd.DataFrame(data,index=[1])
        right_panel.success(f"Customer with ID: {cust_id} have {predict(pd.DataFrame(data))[0]*100.round(2)}% to accept the Personal Loan offer.")
        right_panel.balloons()
