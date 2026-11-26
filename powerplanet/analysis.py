import numpy as np
import pandas as pd
from scipy.stats import linregress, spearmanr

X_COLUMNS = "gdp_per_capita"
Y_COLUMNS = "co2_per_capita"


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
