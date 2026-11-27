"""Cached tables shared by the Streamlit pages."""

import pandas as pd
import streamlit as st

from powerplanet.cleaning import (
    add_energy_shares,
    add_gdp_per_capita,
    merge_co2_and_energy,
    split_countries_aggregates,
)
from powerplanet.loader import load_co2_data, load_energy_data


@st.cache_data
def get_energy_mix() -> pd.DataFrame:
    """Return CO2 data merged with the energy mix and its shares.

    Returns
    -------
    pd.DataFrame
        One row per country or aggregate and year, with *_share columns.

    Raises
    ------
    DataLoadError
        If a data file cannot be downloaded or read.
    """
    return add_energy_shares(merge_co2_and_energy(load_co2_data(), load_energy_data()))


@st.cache_data
def get_countries() -> pd.DataFrame:
    """Return CO2 data for countries only, with GDP per capita.

    Returns
    -------
    pd.DataFrame
        One row per country and year, aggregates removed.

    Raises
    ------
    DataLoadError
        If the CO2 data file cannot be downloaded or read.
    """
    countries, _ = split_countries_aggregates(add_gdp_per_capita(load_co2_data()))
    return countries
