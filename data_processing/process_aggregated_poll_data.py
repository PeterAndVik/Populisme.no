import os
import pandas as pd
import plotly.express as px

# Define file paths
CLEANED_FILE = "data/processed/poll_data_clean.csv"
GRAPH_HTML_FILE = "graphs/aggregated_poll_trends.html"

# Check if cleaned file exists
if not os.path.exists(CLEANED_FILE):
    print(f"⚠️ Cleaned file not found: {CLEANED_FILE}")
    exit()

# Read cleaned poll data
df_polls = pd.read_csv(CLEANED_FILE, index_col="Date", parse_dates=True)

# Filter data from 2014 onwards
df_filtered = df_polls.loc[df_polls.index >= pd.Timestamp('2014-01-01')].copy()

# --- Define Party Groups ---
# Define the party columns for each group
group1_cols = ['Ap', 'HÃ¸yre', 'MDG', 'Venstre']
group2_cols = ['Frp', 'Sp','RÃ¸dt','Andre']

# Sum the percentages for each group (row-wise).
df_filtered['Anywheres (Ap,H,MDG,V)'] = df_filtered[group1_cols].sum(axis=1, min_count=1)
df_filtered['Somewheres (Frp,Sp,R,Andre)'] = df_filtered[group2_cols].sum(axis=1, min_count=1)

# 📊 Generate an interactive line plot with Plotly
fig = px.line(df_filtered, x=df_filtered.index, y=['Anywheres (Ap,H,MDG,V)', 'Somewheres (Frp,Sp,R,Andre)'],
              labels={"value": "Percentage Support", "variable": "Party Groups"},
              title="Aggregated Political Party Support Over Time (2014+)")

# Ensure graphs directory exists
os.makedirs("graphs", exist_ok=True)

# Save the interactive HTML graph
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Aggregated graph saved as HTML: {GRAPH_HTML_FILE}")

# Show the graph for review
fig.show()
