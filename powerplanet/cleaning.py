""" """ 
from powerplanet.loader import ENERGY_SOURCES

import pandas as pd

KEYS = [
    "country",
    "year",]
MIX_COLUMNS = [f"{source}_consumption" for source in ENERGY_SOURCES]

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

def merge_co2_and_energy(co2_df: pd.DataFrame, energy_df: pd.DataFrame) -> pd.DataFrame:
    """Merge CO2 and energy DataFrames on 'country' and 'year'.
    
    Parameters:
        co2_df (pd.DataFrame): The CO2 DataFrame.
        energy_df (pd.DataFrame): The energy DataFrame.
    
    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    energy_mix = energy_df[KEYS + MIX_COLUMNS]
    return co2_df.merge(energy_mix, on=KEYS, how='left', validate='one_to_one')