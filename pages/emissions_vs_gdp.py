"""Page comparing CO2 per capita with GDP per capita across countries."""

import streamlit as st

from powerplanet.analysis import fit_log_log, spearman_correlation
from powerplanet.datasets import get_countries
from powerplanet.loader import DataLoadError
from powerplanet.plots import plot_emissions_vs_gdp

FIRST_YEAR = 1990
LAST_YEAR = 2022

st.title("Emissions vs GDP")

try:
    countries = get_countries()
except DataLoadError as error:
    st.error(f"Could not load data: {error}")
    st.stop()

year = st.slider("Year", FIRST_YEAR, LAST_YEAR, LAST_YEAR)
data = countries[countries["year"] == year]

regression = fit_log_log(data)
correlation = spearman_correlation(data)

left, middle, right = st.columns(3)
left.metric("Slope (log-log)", f"{regression.slope:.2f}")
middle.metric("R²", f"{regression.rvalue ** 2:.2f}")
right.metric("Spearman ρ", f"{correlation.statistic:.2f}")

st.plotly_chart(plot_emissions_vs_gdp(data, regression))
