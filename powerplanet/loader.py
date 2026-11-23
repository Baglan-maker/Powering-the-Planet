"""Module for downloading and loading data files."""
from pathlib import Path

import requests

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
ENERGY_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
TIMEOUT_SECONDS = 30

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