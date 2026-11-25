import plotly.graph_objects as go

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