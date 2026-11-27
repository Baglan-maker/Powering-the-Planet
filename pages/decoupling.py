"""Page classifying countries by decoupling of CO2 from GDP."""

import streamlit as st

from powerplanet.analysis import (
    DECOUPLING_END,
    DECOUPLING_START,
    add_decoupling_category,
    compute_changes,
)
from powerplanet.datasets import get_countries
from powerplanet.plots import plot_category_counts, plot_decoupling

st.title("Decoupling")
st.write(f"Change of GDP and CO2 between {DECOUPLING_START} and {DECOUPLING_END}.")

result = add_decoupling_category(
    compute_changes(get_countries(), DECOUPLING_START, DECOUPLING_END)
)

st.plotly_chart(plot_category_counts(result))
st.plotly_chart(plot_decoupling(result))

category = st.selectbox("Category", sorted(result["category"].unique()))
selected = result[result["category"] == category]
st.dataframe(selected.sort_values("gdp_change", ascending=False).round(1))
