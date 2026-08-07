import streamlit as st

from utils.db import get_companies

st.title("📊 Financial Screener")

companies = get_companies()

st.sidebar.header("Filters")

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    float(companies["roe_percentage"].min()),
    float(companies["roe_percentage"].max()),
    float(companies["roe_percentage"].min())
)

min_roce = st.sidebar.slider(
    "Minimum ROCE (%)",
    float(companies["roce_percentage"].min()),
    float(companies["roce_percentage"].max()),
    float(companies["roce_percentage"].min())
)

filtered = companies[
    (companies["roe_percentage"] >= min_roe) &
    (companies["roce_percentage"] >= min_roce)
]

st.subheader("Filtered Companies")

st.dataframe(
    filtered[
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

st.success(f"{len(filtered)} companies found")