import streamlit as st

from powerplanet.cleaning import split_countries_aggregates
from powerplanet.datasets import get_energy_mix
from powerplanet.plots import plot_energy_mix

DEFAULT_COUNTRY = "Italy"

st.title("Energy Mix")

df = get_energy_mix()
countries, _ = split_countries_aggregates(df)
options = sorted(countries['country'].unique())
country = st.selectbox("Select a country", options, index=options.index(DEFAULT_COUNTRY))
st.plotly_chart(plot_energy_mix(df, country))
