import requests
import pandas as pd
import os

class BaseScraper:
    """
    Base class for all scrapers.
    Handles API requests, error handling, and saving data.
    """
    RAW_DATA_DIR = "data/raw/"

    def __init__(self, filename):
        self.filepath = os.path.join(self.RAW_DATA_DIR, filename)

    def fetch_data(self, url, payload):
        """ Sends a request to the API and returns the JSON response. """
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"🚨 API request failed: {e}")
            return None

    def process_data(self, data):
        """ Must be overridden in each scraper to convert JSON to a DataFrame. """
        raise NotImplementedError("process_data() must be implemented in the subclass")

    def save_to_csv(self, df):
        """ Saves the DataFrame as a CSV file. """
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        df.to_csv(self.filepath, index=False)
        print(f"✅ Data saved to {self.filepath}")

    def run(self):
        """ Runs the entire process: fetch, process, and save. """
        data = self.fetch_data(self.URL, self.PAYLOAD)
        if data:
            df = self.process_data(data)
            self.save_to_csv(df)
