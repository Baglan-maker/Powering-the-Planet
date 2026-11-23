"""Module for downloading and loading data files."""
from pathlib import Path

import requests
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
ENERGY_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
TIMEOUT_SECONDS = 30
CO2_FILE = DATA_DIR / "owid-co2-data.csv"
ENERGY_FILE = DATA_DIR / "owid-energy-data.csv"
CO2_COLUMNS = [
    "country",
    "year",
    "co2",
    "gdp",
    "population",
    "iso_code",
    "co2_per_capita",
]
ENERGY_SOURCES = [
    "coal",
    "oil",
    "gas",
    "nuclear",
    "hydro",
    "solar",
    "wind",
    "biofuel",
    "other_renewable",
]
ENERGY_COLUMNS = [
    "country",
    "year",
    "iso_code",
    "primary_energy_consumption",
    *[f"{source}_consumption" for source in ENERGY_SOURCES],
]


class DataLoadError(Exception):
    """Custom exception for data loading errors."""



def download_file(url: str, destination: Path) -> Path:
    """Download a file from a URL and save it to disk.

    Parameters
    ----------
    url : str
        Address of the file to download.
    destination : pathlib.Path
        Where to save the file.

    Returns
    -------
    pathlib.Path
        The path of the saved file.

    Raises
    ------
    DataLoadError
        If the request times out, the server returns an HTTP error,
        or the connection fails.
    """

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.Timeout as e:
        raise DataLoadError(f"Request timed out after {TIMEOUT_SECONDS} seconds for {url}") from e
    except requests.HTTPError as e:
        raise DataLoadError(f"HTTP {e.response.status_code} error occurred for {url}") from e
    except requests.RequestException as e:
        raise DataLoadError(f"Request failed for {url}: {e}") from e
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)
    return destination


def read_csv(path: Path, required_columns: list[str]) -> pd.DataFrame:
    """Read a CSV file into a pandas DataFrame and check for required columns.
    
    Parameters
    ----------
    path : pathlib.Path
        Path to the CSV file.
    required_columns : list of str
        List of columns that must be present in the DataFrame.     
    
    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.

    Raises
    ------
    DataLoadError
        If the file is not found, cannot be read, or is missing required columns.
    """
    try: 
        df = pd.read_csv(path)
    except FileNotFoundError as e:
        raise DataLoadError(f"File not found: {path}") from e
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        raise DataLoadError(f"Error reading CSV file: {path}") from e
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise DataLoadError(f"Missing required columns in {path}: {missing}")
    return df


def load_dataset(url: str, path: Path, required_columns: list[str]) -> pd.DataFrame:
    """Read a dataset from disk, downloading it first if it is not there yet.

    Parameters
    ----------
    url : str
        Address to download the file from when it is missing.
    path : pathlib.Path
        Where the file is stored locally.
    required_columns : list of str
        Columns that must be present in the file.

    Returns
    -------
    pd.DataFrame
        The loaded dataset.

    Raises
    ------
    DataLoadError
        If the file cannot be downloaded or read, or if required columns are missing.
    """
    if not path.exists():
        download_file(url, path)
    return read_csv(path, required_columns)


def load_co2_data() -> pd.DataFrame:
    """Load CO2 data from the local file or download it if not present.

    Returns
    -------
    pd.DataFrame
        The CO2 data as a pandas DataFrame.

    Raises
    ------
    DataLoadError
        If the file cannot be downloaded or read, or if required columns are missing.
    """
    return load_dataset(CO2_URL, CO2_FILE, CO2_COLUMNS)


def load_energy_data() -> pd.DataFrame:
    """Load energy data from the local file or download it if not present.

    Returns
    -------
    pd.DataFrame
        The energy data as a pandas DataFrame.

    Raises
    ------
    DataLoadError
        If the file cannot be downloaded or read, or if required columns are missing.
    """
    return load_dataset(ENERGY_URL, ENERGY_FILE, ENERGY_COLUMNS)