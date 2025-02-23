import sys
import os
import pandas as pd
import plotly.express as px
# ✅ Ensure correct paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.graph_utils import apply_common_styles  # Import our utility

# 📌 File paths
RAW_FILE = "data/raw/ssb_expenditure_raw.csv"
PROCESSED_FILE = "data/processed/ssb_expenditure_clean.csv"
GRAPH_HTML_FILE = "graphs/ssb_expenditure.html"

# Check if raw file exists
if not os.path.exists(RAW_FILE):
    print(f"⚠️ Raw file not found: {RAW_FILE}")
    exit()

# Read raw data
df = pd.read_csv(RAW_FILE)

# Remove missing values
df = df.dropna()

# Convert 'Year' column to datetime format and sort
df["Year"] = pd.to_datetime(df["Year"], format='%Y')
df.sort_values("Year", inplace=True)

# Ensure processed data directory exists and save cleaned data
os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
df.to_csv(PROCESSED_FILE, index=False)
print(f"✅ Cleaned data saved: {PROCESSED_FILE}")

# Generate interactive graph using Plotly
fig = px.line(
    df,
    x="Year",
    y="Total Expenditure (mill. kr)",
    title="Total Expenditure Over Time (Norwegian State Budget)"
)

# Define a custom hover template
common_hover = "Year: %{x|%Y}<br>Total Expenditure: %{y:.2f} mill. kr<extra></extra>"

# Apply common styles and interactivity enhancements
fig = apply_common_styles(fig, legend_title=None, hover_template=common_hover)

# Ensure graphs directory exists and save the interactive HTML graph
os.makedirs("graphs", exist_ok=True)
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Graph saved as HTML: {GRAPH_HTML_FILE}")

# Show the graph for review
fig.show()
