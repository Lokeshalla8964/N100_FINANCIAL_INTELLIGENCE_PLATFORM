import streamlit as st
import plotly.express as px

from utils.db import get_companies

st.title("🏢 Company Profile")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

selected = companies[companies["company_name"] == company].iloc[0]

st.subheader(company)

col1, col2 = st.columns(2)

with col1:
    st.metric("ROE (%)", selected["roe_percentage"])

with col2:
    st.metric("ROCE (%)", selected["roce_percentage"])

st.write("Website:", selected["website"])
st.write("About Company:")
st.write(selected["about_company"])

chart_data = companies.head(10)

fig = px.bar(
    chart_data,
    x="company_name",
    y=["roe_percentage", "roce_percentage"],
    barmode="group",
    title="ROE vs ROCE"
)

st.plotly_chart(fig, use_container_width=True)