import numpy as np
import pandas as pd
from scipy.stats import linregress, spearmanr

X_COLUMNS = "gdp_per_capita"
Y_COLUMNS = "co2_per_capita"

DECOUPLING_START = 2000
DECOUPLING_END = 2022


def fit_log_log(df: pd.DataFrame):
    """
    Fit a log-log linear regression model to the given DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the data.
    
    
    """

    data = df.dropna(subset=[X_COLUMNS, Y_COLUMNS])
    data = data[(data[X_COLUMNS] > 0) & (data[Y_COLUMNS] > 0)]
    x = np.log10(data[X_COLUMNS])
    y = np.log10(data[Y_COLUMNS])
    return linregress(x, y)

def spearman_correlation(df: pd.DataFrame):
    """Compute the Spearman rank correlation between GDP and CO2 per capita.

    Parameters
    ----------
    df : pd.DataFrame
        Table with gdp_per_capita and co2_per_capita columns.

    Returns
    -------
    scipy.stats.SignificanceResult
        Result with the correlation (statistic) and its p-value (pvalue).
    """

    data = df.dropna(subset=[X_COLUMNS, Y_COLUMNS])
    return spearmanr(data[X_COLUMNS], data[Y_COLUMNS])

def predict_co2(regression, gdp_per_capita: np.ndarray) -> np.ndarray:
    """Predict CO2 per capita from GDP per capita using a log-log fit.

    Parameters
    ----------
    regression : scipy.stats._stats_py.LinregressResult
        Result of fit_log_log.
    gdp_per_capita : np.ndarray
        GDP per capita values to predict for.

    Returns
    -------
    np.ndarray
        Predicted CO2 per capita, in tonnes.
    """

    return 10 ** (regression.intercept + regression.slope * np.log10(gdp_per_capita))

def compute_changes(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    """Compute percent change of GDP and CO2 for each country between two years.

    Parameters
    ----------
    df : pd.DataFrame
        Country rows with country, year, gdp and co2 columns.
    start : int
        First year of the period.
    end : int
        Last year of the period.

    Returns
    -------
    pd.DataFrame
        One row per country (index), columns gdp_change and co2_change in percent.
        Countries with missing values in either year are dropped.
    """
    first = df[df["year"] == start].set_index("country")[["gdp", "co2"]]
    last = df[df["year"] == end].set_index("country")[["gdp", "co2"]]
    changes = (last / first - 1) * 100
    changes.columns = ["gdp_change", "co2_change"]
    return changes.dropna()

def classify_decoupling(gdp_change: float, co2_change: float) -> str:
    """Classify one country's decoupling from its GDP and CO2 change.

    Parameters
    ----------
    gdp_change : float
        Percent change of GDP over the period.
    co2_change : float
        Percent change of CO2 over the period.

    Returns
    -------
    str
        One of "Shrinking economy", "Absolute decoupling",
        "Relative decoupling", "No decoupling".
    """
    
    if gdp_change <= 0:
        return "Shrinking economy"
    elif co2_change < 0:
        return "Absolute decoupling"
    elif co2_change < gdp_change:
        return "Relative decoupling"
    else:
        return "No decoupling"

def add_decoupling_category(changes: pd.DataFrame) -> pd.DataFrame:
    """Add a decoupling category column to the changes table.

    Parameters
    ----------
    changes : pd.DataFrame
        Output of compute_changes.

    Returns
    -------
    pd.DataFrame
        Copy of changes with an extra category column.
    """

    changes = changes.copy()
    changes["category"] = [classify_decoupling(gdp, co2) for gdp, co2 in zip(changes["gdp_change"], changes["co2_change"])]
    return changes
