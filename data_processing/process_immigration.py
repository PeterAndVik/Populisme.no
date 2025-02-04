import os
import pandas as pd
import scipy.ndimage
import plotly.express as px

# ✅ File paths
RAW_FILE = "data/raw/immigration_raw.csv"
PROCESSED_FILE = "data/processed/immigration_clean.csv"
GRAPH_HTML_FILE = "graphs/immigration.html"

# ✅ Ensure raw data exists
if not os.path.exists(RAW_FILE):
    print(f"⚠️ Raw file not found: {RAW_FILE}")
    exit()

# ✅ Load data
df = pd.read_csv(RAW_FILE)

# ✅ Keep only data from 2014 onwards
df_filtered = df[df['år'] >= 2014]

# ✅ Group data by year and sum immigration numbers
df_grouped = df_filtered.groupby('år')['Innvandring'].sum().reset_index()

# ✅ Convert immigration numbers to millions for readability
df_grouped['Innvandring_millions'] = df_grouped['Innvandring'] / 1e6

# ✅ Apply Gaussian smoothing filter
df_grouped['Smoothed_Innvandring'] = scipy.ndimage.gaussian_filter1d(df_grouped['Innvandring_millions'], sigma=2)

# ✅ Ensure processed data directory exists
os.makedirs("data/processed", exist_ok=True)

# ✅ Save cleaned data
df_grouped.to_csv(PROCESSED_FILE, index=False)
print(f"✅ Cleaned data saved: {PROCESSED_FILE}")

# ✅ Create interactive graph
fig = px.line(
    df_grouped,
    x="år",
    y="Smoothed_Innvandring",
    title="Innvandring til Norge (2014-)",
    labels={"år": "År", "Smoothed_Innvandring": "Antall innvandrere (millioner)"},
    line_shape="spline"
)

# ✅ Ensure graphs directory exists
os.makedirs("graphs", exist_ok=True)

# ✅ Save graph as HTML
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Graph saved as HTML: {GRAPH_HTML_FILE}")

# ✅ Show the graph for verification
fig.show()
