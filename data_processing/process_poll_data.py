import os
import pandas as pd
import plotly.express as px

# Define file paths
RAW_FILE = "data/raw/poll_data_raw.csv"
PROCESSED_FILE = "data/processed/poll_data_clean.csv"
GRAPH_HTML_FILE = "graphs/poll_trends.html"

# Check if raw file exists
if not os.path.exists(RAW_FILE):
    print(f"⚠️ Raw file not found: {RAW_FILE}")
    exit()

# Read raw data
df_polls = pd.read_csv(RAW_FILE)

# Rename the first column for clarity
df_polls.rename(columns={'Unnamed: 0': 'Month'}, inplace=True)

# Mapping Norwegian month names to English
norwegian_months = {
    "Januar": "January", "Februar": "February", "Mars": "March",
    "April": "April", "Mai": "May", "Juni": "June",
    "Juli": "July", "August": "August", "September": "September",
    "Oktober": "October", "November": "November", "Desember": "December"
}

# Function to convert the Norwegian month string into a datetime object
def parse_norwegian_date(date_str):
    parts = date_str.split()
    if len(parts) >= 2:
        month_str, year_str = parts[0], parts[1].replace("'", "")
        if len(year_str) == 2:
            year_str = "20" + year_str  # Convert '23 to 2023
        eng_month = norwegian_months.get(month_str, month_str)
        return pd.to_datetime(f"1 {eng_month} {year_str}", format="%d %B %Y")
    return pd.NaT

# Convert the Month column to datetime
df_polls['Date'] = df_polls['Month'].apply(parse_norwegian_date)
df_polls.set_index('Date', inplace=True)

# Clean numeric columns (remove extra text, replace commas, convert to float)
for col in df_polls.columns:
    if col != 'Month':
        df_polls[col] = df_polls[col].astype(str).str.split(' ', expand=True)[0]
        df_polls[col] = df_polls[col].str.replace(',', '.')
        df_polls[col] = pd.to_numeric(df_polls[col], errors='coerce')

# Drop the original Month column
df_polls.drop(columns=["Month"], inplace=True)

# Ensure processed data directory exists
os.makedirs("data/processed", exist_ok=True)

# Save cleaned data
df_polls.to_csv(PROCESSED_FILE)
print(f"✅ Cleaned poll data saved: {PROCESSED_FILE}")

# 📊 Generate an interactive line plot with Plotly
fig = px.line(df_polls, x=df_polls.index, y=df_polls.columns, title="Political Party Support Over Time")

# Ensure graphs directory exists
os.makedirs("graphs", exist_ok=True)

# Save the interactive HTML graph
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Graph saved as HTML: {GRAPH_HTML_FILE}")

# Show the graph for review
fig.show()
