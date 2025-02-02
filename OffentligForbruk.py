import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define the API endpoint
url = "https://data.ssb.no/api/v0/no/table/10487/"

# Define the JSON query payload
payload = {
    "query": [
        {
            "code": "Hovedpost",
            "selection": {
                "filter": "item",
                "values": ["UTG.IALT"]
            }
        },
        {
            "code": "Tid",
            "selection": {
                "filter": "item",
                "values": [
                    "2014", "2015", "2016", "2017", "2018",
                    "2019", "2020", "2021", "2022", "2023",
                    "2024", "2025"
                ]
            }
        }
    ],
    "response": {
        "format": "json-stat2"
    }
}

# Send the request to the API
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract the time periods
    time_periods = data["dimension"]["Tid"]["category"]["label"]

    # Extract the expenditure values
    values = data["value"]

    # Convert to DataFrame
    df = pd.DataFrame({
        "Year": list(time_periods.values()),  # Extracting actual year labels
        "Total Expenditure (mill. kr)": values
    })

    # Print the DataFrame
    print(df)

    # Save as CSV (optional)
    df.to_csv("ssb_expenditure_data.csv", index=False)
    print("Data saved as 'ssb_expenditure_data.csv'")

    # 📊 Plot the expenditure over time
    plt.figure(figsize=(12, 6))
    plt.plot(df["Year"], df["Total Expenditure (mill. kr)"], linestyle='-', linewidth=2)

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("Total Expenditure (mill. kr)")
    plt.title("Total Expenditure Over Time (Norwegian State Budget)")

    # Grid and formatting
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Show the plot
    plt.show()

else:
    print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
