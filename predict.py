import pickle
import sys
import json
import pandas as pd
import streamlit as st

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Load Model
filehandler = open('model_rf.pkl', 'rb')
model = pickle.load(filehandler)

# Streamlit Form
input_form = st.form("Information Form")
input_form.header("Information Form")
name = input_form.text_input("Full Name", placeholder="John Doe")
no_of_dependent = input_form.number_input("Number of Dependents", min_value=0)
education = input_form.selectbox("Education", ("Graduated", "Not Graduated"))
self_employed = input_form.selectbox("Self Employed", ("Yes", "No"))
income_annum = input_form.number_input("Annual Income ($)", min_value=0)
loan_amount = input_form.number_input("Loan Amount ($)", min_value=0)
loan_term = input_form.number_input("Loan Term in Year", min_value=0)
cibil_score = input_form.number_input("Credit Score", min_value=0)
residential_assets_value = input_form.number_input("Residential Asset Value ($)", min_value=0)
commercial_assets_value = input_form.number_input("Commercial Asset Value ($)", min_value=0)
submit_button = input_form.form_submit_button(label="Submit & Predict")

# Encode Education
if education == "Graduated":
    education = 1
else:
    education = 0

# Encode Self Employed
if self_employed == "Yes":
    self_employed = 1
else:
    self_employed = 0

if(submit_button):
       column_name =  ['no_of_dependents', 'education', 'self_employed',
       'income_annum', 'loan_amount', 'loan_term', 'cibil_score',
       'residential_assets_value', 'commercial_assets_value']

       df = pd.DataFrame([[no_of_dependent, education, self_employed, income_annum, loan_amount, loan_term, cibil_score, residential_assets_value, commercial_assets_value]])
       df.columns = column_name

       y = model.predict(df)

       st.table(df)

       first_name = name.split()[0]
       st.write(f"Hello {first_name}")

       if y[0] == 1:
            st.write("Your loan proposal is more likely to be accepted")
       else:
            st.write("Your loan proposal is more likely to be rejected")