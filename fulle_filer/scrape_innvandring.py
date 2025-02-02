import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage

# Load the dataset
url = "https://data.ssb.no/api/v0/dataset/48670.csv?lang=no"
data = pd.read_csv(url, sep=';', decimal=',', encoding="ISO-8859-1")

# Rename the relevant column
data = data.rename(columns={
    "07108: Innvandrere og norskfødte med innvandrerforeldre, etter region, kjønn, landbakgrunn, år og statistikkvariabel": "Innvandring"
})

# Filter data for years 2014 and later
data_filtered = data[data['år'] >= 2014]

# Group data by year and sum the immigration numbers
data_grouped = data_filtered.groupby('år')['Innvandring'].sum().reset_index()

# Convert immigration numbers to millions for readability
data_grouped['Innvandring_millions'] = data_grouped['Innvandring'] / 1e6

# Apply smoothing filter to the data
data_grouped['Smoothed_Innvandring'] = scipy.ndimage.gaussian_filter1d(data_grouped['Innvandring_millions'], sigma=2)

# Plot settings
plt.style.use('default')
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Plot the smoothed immigration trend
ax.plot(
    data_grouped['år'],
    data_grouped['Smoothed_Innvandring'],
    linestyle='-',
    linewidth=2,
    color='tab:blue',
    label='Smoothed Innvandring'
)

# Labels and title
ax.set_xlabel("År", fontsize=14)
ax.set_ylabel("Antall innvandrere (millioner)", fontsize=14)
ax.set_title("Innvandring til Norge (2014-)", fontsize=16, fontweight='bold')

# Grid and formatting
ax.grid(True, linestyle='--', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='major', labelsize=12)
ax.set_xticks(data_grouped['år'])
ax.set_xticklabels(data_grouped['år'], rotation=45)

# Set limits for the y-axis, starting at 0.5
ax.set_ylim(0.5, max(data_grouped['Smoothed_Innvandring']) + 0.1)

# Add legend
ax.legend(fontsize=12)

# Adjust layout
plt.tight_layout()

# Show plot
plt.show()

