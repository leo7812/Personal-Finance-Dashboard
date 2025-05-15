# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# Load or initialize data here
try:
    df = pd.read_csv("transactions.csv", parse_dates=["Date"])
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

# Input form
st.title("💰 Personal Finance Tracker")
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    date_input = col1.date_input("Date", value=date.today())
    category = col2.selectbox("Category", ["Food", "Rent", "Transport", "Entertainment", "Other"])
    amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
    notes = st.text_input("Notes")
    submitted = st.form_submit_button("Add Transaction")
    
    if submitted:
        new_row = pd.DataFrame([[date_input, category, amount, notes]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("transactions.csv", index=False)
        st.success("Transaction added!")

# Dashboard
st.subheader("📅 Monthly Spending Overview")

# Filter current month
df["Date"] = pd.to_datetime(df["Date"])
this_month = df[df["Date"].dt.month == date.today().month]

# Pie Chart by Category
if not this_month.empty:
    cat_totals = this_month.groupby("Category")["Amount"].sum().reset_index()
    fig_pie = px.pie(cat_totals, names="Category", values="Amount", title="Spending by Category")
    st.plotly_chart(fig_pie)

    # Line Chart by Date
    daily_spend = this_month.groupby("Date")["Amount"].sum().reset_index()
    fig_line = px.line(daily_spend, x="Date", y="Amount", title="Daily Spending Trend")
    st.plotly_chart(fig_line)

# Table
st.subheader("📄 All Transactions")
st.dataframe(df.sort_values(by="Date", ascending=False))
