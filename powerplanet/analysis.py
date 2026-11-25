import numpy as np
import pandas as pd
from scipy.stats import linregress

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