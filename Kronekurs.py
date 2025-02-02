import pandas as pd
import requests
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# Define the CSV API URL
url = "https://data.norges-bank.no/api/data/EXR/M.USD.NOK.SP?format=csv&lastNObservations=150&locale=no&bom=include"

# Fetch the CSV data
response = requests.get(url)

# Save the CSV file temporarily
csv_file = "usd_nok_exchange_rates.csv"
with open(csv_file, "wb") as file:
    file.write(response.content)

# Load the CSV file and skip metadata rows
df = pd.read_csv(csv_file, delimiter=";", skiprows=1)  # Adjust skiprows if needed

# Select only the relevant columns (date & exchange rate)
df = df.iloc[:, [-2, -1]]  # Keep only the last two columns

# Rename columns for clarity
df.columns = ["Date", "Exchange Rate"]

# Convert Date column to datetime format
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Convert Exchange Rate to numeric (fix comma issue)
df["Exchange Rate"] = df["Exchange Rate"].str.replace(",", ".").astype(float)

# Sort data by date to ensure proper visualization
df = df.sort_values("Date")

# Apply smoothing to the exchange rate values
df["Smoothed Rate"] = gaussian_filter1d(df["Exchange Rate"], sigma=2)  # Adjust sigma for smoothing effect

# Plot the exchange rate trend with a smoothed line
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["Smoothed Rate"], linestyle='-', linewidth=2, label="Smoothed Exchange Rate")
plt.xlabel("Date")
plt.ylabel("Exchange Rate (USD/NOK)")
plt.title("USD to NOK Exchange Rate Trend (Smoothed)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
