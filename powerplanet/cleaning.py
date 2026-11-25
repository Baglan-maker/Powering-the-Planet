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

def add_energy_shares(df: pd.DataFrame) -> pd.DataFrame:
    """Add energy share columns to the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.DataFrame: The DataFrame with added energy share columns.
    """
    df = df.copy()
    total = df[MIX_COLUMNS].sum(axis=1, skipna=False)
    for source in ENERGY_SOURCES:
        df[f"{source}_share"] = df[f"{source}_consumption"] / total * 100
    return df

def add_gdp_per_capita(df: pd.DataFrame) -> pd.DataFrame:
    """Add GDP per capita column to the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.DataFrame: The DataFrame with added GDP per capita column.
    """
    df = df.copy()
    df['gdp_per_capita'] = df['gdp'] / df['population']
    return df