import os
import pandas as pd
import plotly.express as px

# 📌 Processing Script (data_processing/process_ssb_expenditure.py)
RAW_FILE = "data/raw/ssb_expenditure_raw.csv"
PROCESSED_FILE = "data/processed/ssb_expenditure_clean.csv"
GRAPH_HTML_FILE = "web/graphs/ssb_expenditure.html"

if not os.path.exists(RAW_FILE):
    print(f"⚠️ Raw file not found: {RAW_FILE}")
    exit()

# Read raw data
df = pd.read_csv(RAW_FILE)

# Remove missing values
df = df.dropna()

# Convert 'Year' column to datetime format
df["Year"] = pd.to_datetime(df["Year"], format='%Y')
df.sort_values("Year", inplace=True)

# Ensure processed data directory exists
os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)

# Save cleaned data
df.to_csv(PROCESSED_FILE, index=False)
print(f"✅ Cleaned data saved: {PROCESSED_FILE}")

# 📊 Generate interactive graph using Plotly
fig = px.line(df, x="Year", y="Total Expenditure (mill. kr)", title="Total Expenditure Over Time (Norwegian State Budget)")

# Ensure graphs directory exists
os.makedirs("graphs", exist_ok=True)

# Save the interactive HTML graph
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Graph saved as HTML: {GRAPH_HTML_FILE}")

# Show the graph for review
fig.show()