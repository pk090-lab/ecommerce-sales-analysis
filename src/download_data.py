"""Download and extract the UCI Online Retail workbook."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
TARGET = RAW_DIR / "Online Retail.xlsx"

def main():
    if TARGET.exists():
        print(f"Dataset already exists: {TARGET}")
        return
    print(f"Downloading dataset from {URL}")
    response = requests.get(URL, timeout=90)
    response.raise_for_status()
    with ZipFile(BytesIO(response.content)) as archive:
        candidates = [n for n in archive.namelist() if n.lower().endswith(".xlsx")]
        if not candidates:
            raise RuntimeError("No .xlsx workbook found in downloaded archive. Download manually from the UCI dataset page.")
        with archive.open(candidates[0]) as source, TARGET.open("wb") as dest:
            dest.write(source.read())
    print(f"Saved workbook to {TARGET}")

if __name__ == "__main__":
    main()
