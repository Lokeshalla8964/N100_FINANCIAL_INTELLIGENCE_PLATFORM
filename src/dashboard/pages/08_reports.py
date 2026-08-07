import streamlit as st

from utils.db import (
    get_profit_loss,
    get_balance_sheet,
    get_cash_flow,
)

st.title("📑 Financial Reports")

tab1, tab2, tab3 = st.tabs(
    ["Profit & Loss", "Balance Sheet", "Cash Flow"]
)

with tab1:
    st.subheader("Profit & Loss")
    st.dataframe(get_profit_loss(), use_container_width=True)

with tab2:
    st.subheader("Balance Sheet")
    st.dataframe(get_balance_sheet(), use_container_width=True)

with tab3:
    st.subheader("Cash Flow")
    st.dataframe(get_cash_flow(), use_container_width=True)