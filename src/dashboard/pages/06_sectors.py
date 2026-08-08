import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("📊 Sector Analysis")

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "raw"

sectors = pd.read_excel(DATA_PATH / "sectors.xlsx")

sector_count = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    title="Companies by Sector"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(sector_count, use_container_width=True)