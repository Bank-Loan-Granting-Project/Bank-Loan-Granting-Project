import pickle
import sys
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

st.markdown("# LoanPredictor 🪙")
st.divider()

st.markdown(
    "### Welcome to LoanPredictor!"
)

st.markdown(
    "LoanPredictor is here to help you predict whether your bank loan application is going to be accepted or rejected. The goal is to help you understand your chances and prepare you better for the application process."
)

st.markdown(
    "📜 You can simply fill the form below and get your result in just short amount of time"
)

# Load Model
filehandler = open('model_rf.pkl', 'rb')
model = pickle.load(filehandler)



# Streamlit Form
with st.form("Information Form"):
    st.markdown("### Information Form")
    first_col, second_col = st.columns(2)
    with first_col:
        name = st.text_input("Full Name", placeholder="John Doe",)
        no_of_dependent = st.number_input("Number of Dependents", min_value=0)
        education = st.selectbox("Education", ("Graduated", "Not Graduated"))
        self_employed = st.selectbox("Self Employed", ("Yes", "No"))
        income_annum = st.number_input("Annual Income ($)", min_value=0)
    with second_col:
        loan_amount = st.number_input("Loan Amount ($)", min_value=0)
        loan_term = st.number_input("Loan Term in Year", min_value=0)
        cibil_score = st.number_input("Credit Score", min_value=0)
        residential_assets_value = st.number_input("Residential Asset Value ($)", min_value=0)
        commercial_assets_value = st.number_input("Commercial Asset Value ($)", min_value=0)

    submit_button = st.form_submit_button(label="Submit")

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


def showDataAnalysis(prediction, new_data):
    # load data
    df = pd.read_csv("loan_approval_dataset.csv")
    df.columns = ['loan_id', 'no_of_dependents', 'education', 'self_employed',
    'income_annum', 'loan_amount', 'loan_term', 'cibil_score',
    'residential_assets_value', 'commercial_assets_value',
    'luxury_assets_value', 'bank_asset_value', 'loan_status']

    # append new data to avoid outbound errors
    df = pd.concat([df, new_data], axis=0)



    # make tabs
    tab_loan_st, tab_edu, tab_self_emp, tab_depend, tab_income, tab_loan_am, tab_loan_year, tab_cred_sc, tab_res_val, tab_com_val = st.tabs(["Loan status", "Education", "Self employed", "Number of dependents", "Income", "Loan amount", "Loan term", "Credit score", "Residential asset", "Commercial asset"])

    with tab_loan_st:
        # predict loan_status
        val = df["loan_status"].value_counts()
        pull = [0, 0]
        if prediction == 1:
            pull[1] = pull[1] + 0.2
        else:
            pull[0] = pull[0] + 0.2

        fig = go.Figure(data=[go.Pie(labels=val.index, values=val, pull=pull)])
        st.plotly_chart(fig, theme="streamlit")

    with tab_edu:
        # plot education
        labels = ['Graduated + Approved', 'Graduated + Rejected', 'Not graduated + Approved', 'Not graduated + Rejected']
        values = [
            df[(df["education"] == " Graduate") & (df["loan_status"] == " Approved")].size,
            df[(df["education"] == " Graduate") & (df["loan_status"] == " Rejected")].size,
            df[(df["education"] == " Not Graduate") & (df["loan_status"] == " Approved")].size,
            df[(df["education"] == " Not Graduate") & (df["loan_status"] == " Rejected")].size
        ]
        idx = 0
        pull_values = [0, 0, 0, 0]
        if new_data[new_data["education"] == 1].size == 1:
            if prediction == 1:
                idx = 0
            else:
                idx = 1
        else:
            if prediction == 1:
                idx = 2
            else:
                idx = 3
        pull_values[idx] += 0.2
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull_values)])
        st.plotly_chart(fig)

    with tab_self_emp:
        # predict self_employed
        data = [['self_employed', df['self_employed'].count]]
        fig = px.sunburst(df, path=['self_employed', 'loan_status'], color='loan_status')
        st.plotly_chart(fig)

    with tab_depend:
        # plot no_of_dependents
        data = df["no_of_dependents"].value_counts()
        colors = ['lightslategray',] * data.size
        idx = 0
        for i, j in enumerate(data.index):
            if(j == no_of_dependent):
                idx = i
        colors[i] = 'crimson'
        fig = go.Figure(data=[go.Bar(
            x=data.index,
            y=data,
            marker_color=colors
        )])
        st.plotly_chart(fig)

    with tab_income:
        # plot income_annum
        fig = px.histogram(df, x = "income_annum", color="loan_status", marginal="box", hover_data=df.columns)
        fig.add_vline(x=new_data.income_annum[0], line_dash = 'dash', line_color = 'firebrick')
        st.plotly_chart(fig)

    with tab_loan_am:
        # plot loan_amount
        fig = px.histogram(df, x = "loan_amount", color="loan_status", marginal="rug", hover_data=df.columns)
        fig.add_vline(x=new_data.loan_amount[0], line_dash = 'dash', line_color = 'firebrick')
        st.plotly_chart(fig)

    with tab_loan_year:
        # plot loan_term
        fig = px.histogram(df, x = "loan_term", color="loan_status", marginal="violin", hover_data=df.columns)
        fig.add_vline(x=new_data.loan_term[0], line_dash = 'dash', line_color = 'firebrick')
        st.plotly_chart(fig)

    with tab_cred_sc:
        # plot cibil_score
        fig = px.histogram(df, x = "cibil_score", color="loan_status")
        fig.add_vline(x=new_data.cibil_score[0], line_dash = 'dash', line_color = 'firebrick')
        st.plotly_chart(fig)

    with tab_res_val:
        # plot residential_assets_value
        fig = px.histogram(df, x = "residential_assets_value", color="loan_status")
        fig.add_vline(x=new_data.residential_assets_value[0], line_dash = 'dash', line_color = 'firebrick')
        st.plotly_chart(fig)

    with tab_com_val:
        # plot commercial_assets_value
        fig = px.histogram(df, x = "commercial_assets_value", color="loan_status")
        fig.add_vline(x=new_data.commercial_assets_value[0], line_dash = 'dash', line_color = 'firebrick')
        st.plotly_chart(fig)
    


if(submit_button):
    if(name == ""):
        st.warning("Please input your name")
    else:
        column_name =  ['no_of_dependents', 'education', 'self_employed',
        'income_annum', 'loan_amount', 'loan_term', 'cibil_score',
        'residential_assets_value', 'commercial_assets_value']

        df = pd.DataFrame([[no_of_dependent, education, self_employed, income_annum, loan_amount, loan_term, cibil_score, residential_assets_value, commercial_assets_value]])
        df.columns = column_name

        y = model.predict(df)

        first_name = name.split()[0]
        st.markdown(f"## Hello {first_name}!")

        if y[0] == 1:
            st.markdown("✅ Your loan proposal is more likely to be **accepted**.")
        else:
            st.markdown("❌ Your loan proposal is more likely to be **rejected**.")
        st.markdown("Find out more by analyzing the graphs that we have provided below.")
        
        showDataAnalysis(y[0], df)
