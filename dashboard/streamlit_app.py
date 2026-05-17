"""Dashboard entry point for the Credit Growth Analytics Pipeline.

This file will be implemented after the synthetic data, scoring, and validation
outputs are generated.
"""

import streamlit as st

st.set_page_config(
    page_title="Credit Growth Analytics Pipeline",
    layout="wide",
)

st.title("Credit Growth Analytics Pipeline")
st.caption("Responsible Customer Lifetime Value / Next-Best-Action Model")

st.info(
    "Dashboard scaffold. The executive overview, customer ranking, model "
    "performance, and governance pages will be implemented after the modelling "
    "outputs are generated."
)
