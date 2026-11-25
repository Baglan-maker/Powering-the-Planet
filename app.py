"""Entry point of the Streamlit app: only declares the pages."""
import streamlit as st

st.set_page_config(page_title="Powering the Planet", page_icon="🌍", layout="wide")
pages = [
    st.Page("pages/decoupling.py", title="Decoupling"),
    st.Page("pages/energy_mix.py", title="Energy Mix"),
    st.Page("pages/emissions_vs_gdp.py", title="Emissions vs GDP"),
]
st.navigation(pages=pages).run()