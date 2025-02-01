import pandas as pd
import plotly.express as px
import os
import re

# Ensure the 'graphs' directory exists (not needed but kept for compatibility)
os.makedirs("graphs", exist_ok=True)

# URL of polling data
url = "https://www.pollofpolls.no/?cmd=Stortinget&do=visallesnitt"

# Read tables from the URL
tables = pd.read_html(url)
df_polls = tables[0]  # Select the first table

# Rename the first column for clarity
df_polls.rename(columns={'Unnamed: 0': 'Month'}, inplace=True)

# --- Fix Encoding Issues in Column Names ---
df_polls.rename(columns=lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x, inplace=True)

# Manual Fix for Specific Columns
column_map = {
    "HÃ¸yre": "Høyre",
    "RÃ¸dt": "Rødt",
    "Andre": "Andre",
}
df_polls.rename(columns=column_map, inplace=True)

# Print updated column names for debugging
print("Updated Column Names:", df_polls.columns)

# Mapping Norwegian month names to English
norwegian_months = {
    "Januar": "January", "Februar": "February", "Mars": "March",
    "April": "April", "Mai": "May", "Juni": "June",
    "Juli": "July", "August": "August", "September": "September",
    "Oktober": "October", "November": "November", "Desember": "December"
}

# Function to convert Norwegian month-year string to datetime
def parse_norwegian_date(date_str):
    parts = date_str.split()
    if len(parts) >= 2:
        month_str = parts[0]
        year_str = parts[1].replace("'", "")  # Remove the apostrophe
        if len(year_str) == 2:
            year_str = "20" + year_str  # Convert '24' to '2024'
        eng_month = norwegian_months.get(month_str, month_str)
        date_formatted = f"1 {eng_month} {year_str}"
        return pd.to_datetime(date_formatted, format="%d %B %Y")
    else:
        return pd.NaT

# Convert 'Month' column to datetime format
df_polls['Date'] = df_polls['Month'].apply(parse_norwegian_date)
df_polls.set_index('Date', inplace=True)

# Clean the party columns (remove extra text and convert to float)
for col in df_polls.columns:
    if col != 'Month':  # Skip month column
        df_polls[col] = df_polls[col].astype(str).str.split(' ', expand=True)[0]  # Remove seat numbers
        df_polls[col] = df_polls[col].str.replace(',', '.')  # Fix decimal format
        df_polls[col] = pd.to_numeric(df_polls[col], errors='coerce')  # Convert to float

# Print cleaned data for debugging
print(df_polls.head())

# Define party groups
group1_cols = ['Ap', 'Høyre', 'MDG', 'Venstre']
group2_cols = ['Frp', 'Sp', 'Andre', 'Rødt']

# Check if all required columns exist before summing
missing_cols = [col for col in group1_cols + group2_cols if col not in df_polls.columns]
if missing_cols:
    print(f"Warning: Missing columns - {missing_cols}")
else:
    df_polls['Somewheres'] = df_polls[group1_cols].sum(axis=1)
    df_polls['Anywheres'] = df_polls[group2_cols].sum(axis=1)

# Create an interactive Plotly graph
fig = px.line(df_polls, x=df_polls.index, y=['Somewheres', 'Anywheres'],
              labels={"value": "Percentage Support", "variable": "Party Group"},
              title="Aggregated Political Party Support Over Time")

# Save as an interactive HTML file (in the root folder for GitHub Pages)
fig.write_html("graphs/graph1.html")  # Saves in graphs/ folder

print("Graph updated successfully!")
