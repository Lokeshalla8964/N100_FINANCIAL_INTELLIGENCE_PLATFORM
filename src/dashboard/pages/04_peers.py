import streamlit as st
import plotly.express as px

from utils.db import get_companies

st.title("🤝 Peer Comparison")

companies = get_companies()

selected = st.multiselect(
    "Select Companies",
    companies["company_name"],
    default=companies["company_name"].head(5)
)

peer_df = companies[companies["company_name"].isin(selected)]

st.dataframe(
    peer_df[
        [
            "company_name",
            "roe_percentage",
            "roce_percentage",
            "book_value",
            "face_value"
        ]
    ],
    use_container_width=True
)

import pandas as pd

peer_df["roe_percentage"] = pd.to_numeric(peer_df["roe_percentage"])
peer_df["roce_percentage"] = pd.to_numeric(peer_df["roce_percentage"])

plot_df = peer_df.melt(
    id_vars="company_name",
    value_vars=["roe_percentage", "roce_percentage"],
    var_name="Metric",
    value_name="Percentage"
)

fig = px.bar(
    plot_df,
    x="company_name",
    y="Percentage",
    color="Metric",
    barmode="group",
    title="ROE vs ROCE Comparison"
)

st.plotly_chart(fig, use_container_width=True)