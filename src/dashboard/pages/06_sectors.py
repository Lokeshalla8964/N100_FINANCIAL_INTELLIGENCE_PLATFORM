import streamlit as st
import plotly.express as px

from utils.db import get_companies

st.title("🏭 Sector Analysis")

companies = get_companies()

if "sector" not in companies.columns:
    companies["sector"] = "Unknown"

sector_count = (
    companies.groupby("sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="sector",
    values="Companies",
    title="Companies by Sector"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(sector_count, use_container_width=True)