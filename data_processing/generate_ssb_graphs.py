import pandas as pd
import plotly.express as px
import os
import plotly.io as pio

# Force Plotly to recognize Kaleido
pio.kaleido.scope.mathjax = None  

# Get project root dynamically
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "ssb_expenditure_processed.csv")
GRAPH_DIR = os.path.join(PROJECT_ROOT, "graphs")
INTERACTIVE_DIR = os.path.join(GRAPH_DIR, "interactive")
PNG_PATH = os.path.join(GRAPH_DIR, "ssb_expenditure.png")
HTML_PATH = os.path.join(INTERACTIVE_DIR, "ssb_expenditure.html")

# Ensure directories exist
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(INTERACTIVE_DIR, exist_ok=True)

# Load processed data
df = pd.read_csv(PROCESSED_DATA_PATH)

# Create interactive plot
fig = px.line(df, x="Year", y="Total Expenditure (mill. kr)", 
              title="Total Expenditure Over Time (Norwegian State Budget)",
              labels={"Year": "Year", "Total Expenditure (mill. kr)": "Total Expenditure (mill. kr)"})

# Save interactive HTML
fig.write_html(HTML_PATH)
print(f"✅ Interactive graph saved to {HTML_PATH}")

# Debugging: Print before saving PNG
print(f"📢 Saving PNG to: {PNG_PATH}")

# Save PNG
fig.write_image(PNG_PATH)

# Debugging: Print after saving PNG
print(f"✅ Static PNG graph saved to {PNG_PATH}")
