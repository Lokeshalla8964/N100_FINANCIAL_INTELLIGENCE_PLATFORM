import streamlit as st
import plotly.express as px

from utils.db import get_companies

st.title("📈 Financial Trends")

companies = get_companies()

metric = st.selectbox(
    "Select Metric",
    [
        "roe_percentage",
        "roce_percentage",
        "book_value",
        "face_value"
    ]
)

top = companies.sort_values(metric, ascending=False).head(10)

fig = px.bar(
    top,
    x="company_name",
    y=metric,
    title=f"Top 10 Companies by {metric}"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    top[
        [
            "company_name",
            metric
        ]
    ],
    use_container_width=True
)