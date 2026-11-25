import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from powerplanet.loader import ENERGY_SOURCES

SHARE_COLUMNS = [f"{source}_share" for source in ENERGY_SOURCES]

TEMPLATE = "plotly_white"
FONT_SIZE = 14

def apply_style(fig: go.Figure) -> go.Figure:
    """
    Apply a consistent style to the given Plotly figure.

    Parameters:
    fig (go.Figure): The Plotly figure to style.

    Returns:
    go.Figure: The styled Plotly figure.
    """
    fig.update_layout(
        template=TEMPLATE,
        font=dict(size=FONT_SIZE),
        legend_title_text=None,
    )
    return fig

def plot_energy_mix(df: pd.DataFrame, country: str) -> go.Figure:
    """
    Plot the energy mix for a given country.

    Parameters:
    df (pd.DataFrame): The DataFrame containing energy data.
    country (str): The country for which to plot the energy mix.

    Returns:
    go.Figure: The Plotly figure representing the energy mix.
    """
    data = df[df['country'] == country]
    long = data.melt(id_vars=['year'], value_vars=SHARE_COLUMNS, var_name='source', value_name='share')
    fig = px.area(long, x='year', y='share', color='source', labels={'share': 'Energy Share (%)', 'year': 'Year'})
    return apply_style(fig)
