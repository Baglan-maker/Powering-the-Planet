""" """ 
import pandas as pd

def split_countries_aggregates(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the DataFrame into two parts: one with country data and another with aggregate data.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the DataFrame with country data and the DataFrame with aggregate data.
    """
    is_country = df['iso_code'].notnull()
    countries = df[is_country]
    aggregates = df[~is_country]
    return countries, aggregates