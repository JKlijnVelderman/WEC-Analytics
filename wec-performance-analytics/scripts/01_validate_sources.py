import json
from datetime import datetime, timezone
from pathlib import Path

import openwec
import pandas as pd
from dotenv import load_dotenv
import os


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SERIES = "WEC"
SEASON = 2025
EVENT = "Spa"
SESSION_TYPE = "Race"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENWEC_API_KEY")

if api_key:
    openwec.configure(api_key=api_key)


# --------------------------------------------------
# LOAD SESSION
# --------------------------------------------------

print("=" * 55)
print("WEC PERFORMANCE ANALYTICS")
print("DATA SOURCE VALIDATION")
print("=" * 55)

print("\nConnecting to OpenWEC...")

session = openwec.Session(
    SERIES,
    SEASON,
    EVENT,
    SESSION_TYPE
)

print(f"\nSession identified: {session}")


# --------------------------------------------------
# RETRIEVE CLASSIFICATION
# --------------------------------------------------

print("\nRetrieving race classification...")

results = session.results()

if results is None or results.empty:
    raise RuntimeError("No classification data returned.")

print("\nAvailable columns:")
print(results.columns.tolist())

print("\nClassification preview:")
print(results.head(10).to_string(index=False))


# --------------------------------------------------
# BASIC VALIDATION
# --------------------------------------------------

required_columns = {
    "position",
    "car_number",
    "car_class",
    "team",
    "drivers"
}

missing_columns = required_columns - set(results.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

assert not results["car_number"].isna().any(), (
    "Missing car numbers detected."
)

assert results["car_number"].is_unique, (
    "Duplicate car numbers detected."
)

print("\nBasic validation passed.")


# --------------------------------------------------
# IDENTIFY WRT ENTRIES
# --------------------------------------------------

wrt_entries = results[
    results["team"].str.contains(
        "WRT",
        case=False,
        na=False
    )
]

print("\nWRT entries:")
print(wrt_entries.to_string(index=False))


# --------------------------------------------------
# SAVE RAW CLASSIFICATION
# --------------------------------------------------

output_file = RAW_DIR / "spa_2025_race_classification.csv"

results.to_csv(output_file, index=False)

print(f"\nClassification saved to: {output_file}")


# --------------------------------------------------
# SAVE SOURCE METADATA
# --------------------------------------------------

metadata = {
    "source": "OpenWEC",
    "series": SERIES,
    "season": SEASON,
    "event": EVENT,
    "session": SESSION_TYPE,
    "retrieved_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "record_count": len(results),
    "columns": results.columns.tolist(),
    "api_key_configured": bool(api_key),
    "validation_status": "passed"
}

metadata_file = (
    METADATA_DIR / "spa_2025_source_metadata.json"
)

with open(metadata_file, "w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=4)

print("\nMetadata saved.")
print("\nDATA SOURCE VALIDATION COMPLETE.")