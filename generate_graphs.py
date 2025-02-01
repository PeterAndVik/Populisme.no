import pandas as pd
import numpy as np
import plotly.express as px
import os

# Ensure the 'graphs' directory exists
os.makedirs("graphs", exist_ok=True)

# Generate random test data
np.random.seed(42)
df = pd.DataFrame({
    "Time": pd.date_range(start="2024-01-01", periods=30, freq="D"),
    "Value": np.random.randint(50, 150, size=30)
})

# Create an interactive line chart using Plotly
fig = px.line(df, x="Time", y="Value", title="Random Data Over Time")

# Save the interactive graph as an HTML file
fig.write_html("graphs/graph1.html")

print("Graph saved successfully in graphs/graph1.html")
