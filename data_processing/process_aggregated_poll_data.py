import sys
import os
import pandas as pd
import plotly.express as px
# ✅ Ensure correct paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.graph_utils import apply_common_styles  # Import our utility

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

# Define Party Groups
group1_cols = ['Ap', 'Høyre', 'MDG', 'Venstre']
group2_cols = ['Frp', 'Sp', 'Rødt', 'Andre']
df_filtered['Anywheres (Ap,H,MDG,V)'] = df_filtered[group1_cols].sum(axis=1, min_count=1)
df_filtered['Somewheres (Frp,Sp,R,Andre)'] = df_filtered[group2_cols].sum(axis=1, min_count=1)

# Reset index for clarity
df_filtered = df_filtered.reset_index()

# Generate the interactive line plot
fig = px.line(
    df_filtered,
    x="Date",
    y=['Anywheres (Ap,H,MDG,V)', 'Somewheres (Frp,Sp,R,Andre)'],
    labels={"value": "Percentage Support", "variable": "Party Groups"},
    title="Aggregated Political Party Support Over Time (2014+)"
)

# Apply common styles and interactivity
common_hover = "Date: %{x|%Y-%m-%d}<br>Support: %{y:.2f}%<extra></extra>"
fig = apply_common_styles(fig, legend_title="Party Groups", hover_template=common_hover)

# Ensure graphs directory exists
os.makedirs("graphs", exist_ok=True)
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Aggregated graph saved as HTML: {GRAPH_HTML_FILE}")

# Show the graph for review
fig.show()
