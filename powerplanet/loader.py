from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
ENERGY_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
TIMEOUT_SECONDS = 30

class DataLoadError(Exception):
    """Custom exception for data loading errors."""
    pass