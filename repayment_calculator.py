import pandas as pd
import streamlit as st
import locale
import numpy as np

def number_to_format(number):
    locale.setlocale(locale.LC_ALL, '')
    return locale.currency(number, grouping=True)

def format_to_number(format):
    return int(locale.delocalize(format))

def calculate_repayment(principal, interest_rate, loan_term):
    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12

    # Calculate the monthly repayment
    numerator = monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments
    denominator = (1 + monthly_interest_rate) ** num_payments - 1
    monthly_repayment = principal * (numerator / denominator)

    # Calculate the total repayment over the loan term
    total_repayment = monthly_repayment * num_payments

    return monthly_repayment, total_repayment

def remaining(loan_term, interest_rate, principal, monthly_repayment):
    years_remaining = []
    principal_remaining = []

    monthly_repayment_rate = interest_rate / 12.0 / 100.0

    years_remaining.append(loan_term)
    principal_remaining.append(principal)

    pay = monthly_repayment - principal * monthly_repayment_rate
    principal = principal - pay

    for i in range(loan_term - 1, 0, -1):
        for j in range(0, 12):
            pay = monthly_repayment - principal * monthly_repayment_rate
            principal = principal - pay
        years_remaining.append(i)
        principal_remaining.append(principal)
    years_remaining.append(0)
    principal_remaining.append(0)

    return pd.DataFrame({'years_remaining':years_remaining, 'principal_remaining':principal_remaining})

##############################################

with st.form("form"):
    principal = st.number_input("Loan Amount", value=300000.00, step=100000.0)

    loan_term_years = int(st.number_input("Years", value=30.0, step=1.0))
    type = st.selectbox("Repayment type", ["Principal and interest",
                                        "Interest only 1 year",
                                        "Interest only 2 years",
                                        "Interest only 3 years",
                                        "Interest only 4 years",
                                        "Interest only 5 years"])
    interest_rate = st.number_input("With an interest rate of", value=8.55, step=0.05)
    submit = st.form_submit_button("Submit")

if submit and principal and loan_term_years and interest_rate:
    monthly_repayment, total_repayment = calculate_repayment(principal, interest_rate, loan_term_years)
    remaining_df = remaining(loan_term_years, interest_rate, principal, monthly_repayment)

    st.divider()
    st.title(f"Monthly: {number_to_format(monthly_repayment)}")
    st.title(f"Total repayment:{number_to_format(total_repayment)}")
    st.divider()
    st.line_chart(data=remaining_df)
    st.divider()
    st.table(remaining_df)
