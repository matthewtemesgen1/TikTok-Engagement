from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

def get_raw_path(filename: str):
    """Return the full path to a raw data file."""
    return RAW_DATA_DIR / filename

def get_processed_path(filename: str):
    """Return the full path to a processed data file."""
    return PROCESSED_DATA_DIR / filename