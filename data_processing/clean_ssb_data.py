import pandas as pd
import os

# Define paths relative to project root
RAW_DATA_PATH = "data/raw/ssb_expenditure_raw.csv"
PROCESSED_DATA_PATH = "data/processed/ssb_expenditure_processed.csv"

# Load raw data
df = pd.read_csv(RAW_DATA_PATH)

# Convert Year to integer (if needed)
df["Year"] = df["Year"].astype(int)

# Ensure processed directory exists
os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)

# Save processed data
df.to_csv(PROCESSED_DATA_PATH, index=False)
print(f"✅ Processed data saved to {PROCESSED_DATA_PATH}")
