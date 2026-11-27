import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from powerplanet.loader import ENERGY_SOURCES
from powerplanet.analysis import predict_co2

SHARE_COLUMNS = [f"{source}_share" for source in ENERGY_SOURCES]

CATEGORY_COLORS = {
    "Absolute decoupling": "#2ca02c",
    "Relative decoupling": "#98df8a",
    "No decoupling": "#d62728",
    "Shrinking economy": "#7f7f7f",
}

TEMPLATE = "plotly_dark"
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
    long["source"] = long["source"].str.removesuffix("_share").str.replace("_", " ").str.capitalize()
    fig = px.area(long, x='year', y='share', color='source', labels={'share': 'Energy Share (%)', 'year': 'Year'})
    return apply_style(fig)

def plot_emissions_vs_gdp(df: pd.DataFrame, regression) -> go.Figure:
    """Scatter plot of CO2 vs GDP per capita with the log-log fit line.

    Parameters
    ----------
    df : pd.DataFrame
        Countries for one year, with gdp_per_capita and co2_per_capita.
    regression : scipy.stats._stats_py.LinregressResult
        Result of fit_log_log for the same data.

    Returns
    -------
    go.Figure
        Styled Plotly figure.
    """

    fig = px.scatter(df, x="gdp_per_capita", y="co2_per_capita", hover_name="country",
                        log_x=True, log_y=True, labels={"gdp_per_capita": "GDP per capita (USD)", "co2_per_capita": "CO2 per capita (tonnes)"})
    gdp = np.geomspace(df["gdp_per_capita"].min(), df["gdp_per_capita"].max(), 50)
    fig.add_scatter(x=gdp, y=predict_co2(regression, gdp), mode="lines", name="Log-Log Fit", line=dict(color="red"))
    return apply_style(fig)


def plot_category_counts(result: pd.DataFrame) -> go.Figure:
    """Bar chart of how many countries fall into each decoupling category.

    Parameters
    ----------
    result : pd.DataFrame
        Output of add_decoupling_category.

    Returns
    -------
    go.Figure
        Styled Plotly figure.
    """

    counts = result["category"].value_counts().reset_index()
    counts.columns = ["category", "count"]
    fig = px.bar(counts, x="category", y="count", color="category", color_discrete_map=CATEGORY_COLORS,
                 labels={"category": "", "count": "Countries"})
    fig.update_layout(showlegend=False)
    return apply_style(fig)


def plot_decoupling(result: pd.DataFrame) -> go.Figure:
    """Scatter plot of GDP change vs CO2 change, colored by decoupling category.

    Parameters
    ----------
    result : pd.DataFrame
        Output of add_decoupling_category, indexed by country.

    Returns
    -------
    go.Figure
        Styled Plotly figure with reference lines for zero CO2 change
        and equal GDP and CO2 change.
    """

    data = result.reset_index()
    fig = px.scatter(data, x="gdp_change", y="co2_change",
                        color="category", hover_name="country", color_discrete_map=CATEGORY_COLORS,
                        labels={"gdp_change": "GDP change (%)", "co2_change": "CO2 change (%)"})
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    limit = data["gdp_change"].max()
    fig.add_scatter(x=[0, limit], y=[0, limit], mode="lines", line=dict(color="gray", dash="dot"), name="CO2 = GDP")
    return apply_style(fig)