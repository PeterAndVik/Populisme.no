import requests
import pandas as pd
import os

# Define paths
RAW_DATA_PATH = "data/raw/ssb_expenditure_raw.csv"

# Define the API endpoint
url = "https://data.ssb.no/api/v0/no/table/10487/"

# Define the JSON query payload
payload = {
    "query": [
        {
            "code": "Hovedpost",
            "selection": {"filter": "item", "values": ["UTG.IALT"]}
        },
        {
            "code": "Tid",
            "selection": {
                "filter": "item",
                "values": ["2014", "2015", "2016", "2017", "2018",
                           "2019", "2020", "2021", "2022", "2023",
                           "2024", "2025"]
            }
        }
    ],
    "response": {"format": "json-stat2"}
}

# Send the request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract time periods and values
    time_periods = data["dimension"]["Tid"]["category"]["label"]
    values = data["value"]

    # Convert to DataFrame
    df = pd.DataFrame({"Year": list(time_periods.values()), "Total Expenditure (mill. kr)": values})

    # Ensure the directory exists
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)

    # Save as CSV
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Raw data saved to {RAW_DATA_PATH}")

else:
    print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
