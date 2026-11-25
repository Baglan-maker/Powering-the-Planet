import streamlit as st

from powerplanet.cleaning import split_countries_aggregates, merge_co2_and_energy, add_energy_shares
from powerplanet.loader import load_energy_data, load_co2_data
from powerplanet.plots import plot_energy_mix

DEFAULT_COUNTRY = "Italy"

st.title("Energy Mix")

df = add_energy_shares(merge_co2_and_energy(load_co2_data(), load_energy_data()))
countries, _ = split_countries_aggregates(df)
options = sorted(countries['country'].unique())
country = st.selectbox("Select a country", options, index=options.index(DEFAULT_COUNTRY))
st.plotly_chart(plot_energy_mix(df, country))
