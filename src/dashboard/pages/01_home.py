import streamlit as st
import plotly.express as px

from utils.db import get_companies, get_analysis

st.title("🏠 Financial Intelligence Dashboard")

companies = get_companies()
analysis = get_analysis()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Companies", len(companies))

with col2:
    st.metric("Analysis Records", len(analysis))

st.subheader("Company List")
st.dataframe(companies.head(10), use_container_width=True)

if "roe_percentage" in companies.columns:
    chart = px.histogram(companies, x="roe_percentage", title="ROE Distribution")
    st.plotly_chart(chart, use_container_width=True)