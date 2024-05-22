st.markdown("### Information Form")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Full Name", placeholder="John Doe")
        no_of_dependent = st.slider("Number of dependents", 0, 20, 0)
        # st.number_input("Number of Dependents", min_value=0)
        col11, col12 = st.columns(2)
        with col11:
            education = st.radio("Education", ["Graduated", "Not graduated"])
        # st.selectbox("Education", ("Graduated", "Not Graduated"))
        with col12:
            self_employed = st.radio("Self Employed", ["Yes", "No"])
        # st.selectbox("Self Employed", ("Yes", "No"))
    with col2:
        income_annum = st.number_input("Annual Income ($)", min_value=0)
        loan_amount = st.number_input("Loan Amount ($)", min_value=0)
        loan_term = st.slider("Loan Term in Year", 0, 20, 0)
        # st.number_input("Loan Term in Year", min_value=0)
    with col3:
        cibil_score = st.number_input("Credit Score", min_value=0)
        residential_assets_value = st.number_input("Residential Asset Value ($)", min_value=0)
        commercial_assets_value = st.number_input("Commercial Asset Value ($)", min_value=0)

    st.write("")
    submit_button = st.form_submit_button(label="Submit", on_click=form_callback)


st.markdown("### Information Form")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="John Doe")
        income_annum = st.number_input("Annual Income ($)", min_value=0)
        no_of_dependent = st.slider("Number of dependents", 0, 20, 0)
        col11, col12 = st.columns(2)
        with col11:
            education = st.radio("Education", ["Graduated", "Not graduated"])
        with col12:
            self_employed = st.radio("Self Employed", ["Yes", "No"])
    with col2:
        col21, col22 = st.columns(2)
        with col21:
            loan_amount = st.number_input("Loan Amount ($)", min_value=0)
        with col22:
            loan_term = st.slider("Loan Term in Year", 0, 20, 0)
        cibil_score = st.number_input("Credit Score", min_value=0)
        residential_assets_value = st.number_input("Residential Asset Value ($)", min_value=0)
        commercial_assets_value = st.number_input("Commercial Asset Value ($)", min_value=0)

    st.write("")
    submit_button = st.form_submit_button(label="Submit", on_click=form_callback)


def show_edu(prediction, df, new_data):
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
    return fig

def show_self_emp(prediction, df, new_data):
    data = [['self_employed', df['self_employed'].count]]
    fig = px.sunburst(df, path=['self_employed', 'loan_status'], color='loan_status')
    fig.update_traces(textinfo="label+percent parent", insidetextorientation='horizontal')
    return fig