import os
import sys
import pandas as pd
import plotly.express as px
# ✅ Ensure correct paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.graph_utils import apply_common_styles  # Import our utility
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

# Manually Replace Corrupted Norwegian Letters in Column Names
column_fix_map = {
    "HÃ¸yre": "Høyre",
    "RÃ¸dt": "Rødt",
    "KrF": "KrF",       # Correct, kept for reference
    "Venstre": "Venstre",  # Already correct
    "Andre": "Andre"       # Already correct
}
df_polls.rename(columns=column_fix_map, inplace=True)

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

# Convert the Month column to datetime and set as index
df_polls['Date'] = df_polls['Month'].apply(parse_norwegian_date)
df_polls.set_index('Date', inplace=True)

# Clean numeric columns (remove extra text, replace commas, and convert to float)
for col in df_polls.columns:
    if col != 'Month':
        df_polls[col] = df_polls[col].astype(str).str.split(' ', expand=True)[0]
        df_polls[col] = df_polls[col].str.replace(',', '.')
        df_polls[col] = pd.to_numeric(df_polls[col], errors='coerce')

# Drop the original Month column
df_polls.drop(columns=["Month"], inplace=True)

# Ensure processed data directory exists and save cleaned data
os.makedirs("data/processed", exist_ok=True)
df_polls.to_csv(PROCESSED_FILE)
print(f"✅ Cleaned poll data saved: {PROCESSED_FILE}")

# Generate an interactive line plot with Plotly
fig = px.line(
    df_polls,
    x=df_polls.index,
    y=df_polls.columns,
    title="Political Party Support Over Time"
)

# Apply common styles and interactivity enhancements:
# - Adds a range slider for the x-axis.
# - Sets a custom hover template for consistent tooltips.
common_hover = "Date: %{x|%Y-%m-%d}<br>Support: %{y:.2f}%<extra></extra>"
fig = apply_common_styles(fig, legend_title="Political Parties", hover_template=common_hover)

# Ensure graphs directory exists and save the interactive HTML graph
os.makedirs("graphs", exist_ok=True)
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Graph saved as HTML: {GRAPH_HTML_FILE}")

# Show the graph for review
fig.show()
