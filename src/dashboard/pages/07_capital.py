import streamlit as st
import plotly.express as px

from utils.db import get_companies

st.title("💰 Capital Analysis")

companies = get_companies()

fig = px.scatter(
    companies,
    x="book_value",
    y="face_value",
    hover_name="company_name",
    title="Book Value vs Face Value"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    companies[["company_name", "book_value", "face_value"]],
    use_container_width=True
)