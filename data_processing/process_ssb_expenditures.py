import os
import pandas as pd
import plotly.express as px

# 📌 Processing Script (data_processing/process_ssb_expenditure.py)
RAW_FILE = "data/raw/ssb_expenditure_raw.csv"
PROCESSED_FILE = "data/processed/ssb_expenditure_clean.csv"
GRAPH_HTML_FILE = "graphs/ssb_expenditure.html"

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

# 📊 Generate interactive graph using Plotly with Seaborn-style design
fig = px.line(
    df,
    x="Year",
    y="Total Expenditure (mill. kr)",
    title="Total Expenditure Over Time (Norwegian State Budget)",
    template="plotly_white",  # Clean Seaborn-like theme
    line_shape="spline",  # Smooth line instead of jagged steps
)

# Customize layout for better readability
fig.update_traces(line=dict(width=2.5, color="royalblue"))  # Thicker blue line
fig.update_layout(
    title_font=dict(size=20, family="Arial", color="black"),
    xaxis_title="Year",
    yaxis_title="Total Expenditure (mill. kr)",
    xaxis=dict(showgrid=True, gridcolor="lightgrey"),
    yaxis=dict(showgrid=True, gridcolor="lightgrey"),
    plot_bgcolor="white",
    hovermode="x unified",  # Show hover info across the x-axis
)

# Ensure graphs directory exists
os.makedirs("graphs", exist_ok=True)

# Save the interactive HTML graph
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Graph saved as HTML: {GRAPH_HTML_FILE}")

# Show the graph for review
fig.show()
