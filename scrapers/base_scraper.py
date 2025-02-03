import requests
import pandas as pd
import os

class BaseScraper:
    """
    Base class for all scrapers.
    Supports API requests and HTML table scraping.
    """
    RAW_DATA_DIR = "data/raw/"

    def __init__(self, filename):
        self.filepath = os.path.join(self.RAW_DATA_DIR, filename)

    def fetch_api_data(self, url, payload=None):
        """ Sends a request to an API and returns the JSON response. """
        try:
            response = requests.post(url, json=payload) if payload else requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"🚨 API request failed: {e}")
            return None

    def fetch_html_table(self, url):
        """ Scrapes all tables from an HTML page and returns the first one as a DataFrame. """
        try:
            tables = pd.read_html(url)
            if tables:
                return tables[0]  # Assume the first table is the relevant one
            print("⚠️ No tables found on the webpage.")
            return None
        except Exception as e:
            print(f"🚨 Failed to scrape HTML tables: {e}")
            return None

    def process_data(self, data):
        """ Must be overridden in each scraper to process data. """
        raise NotImplementedError("process_data() must be implemented in the subclass")

    def save_to_csv(self, df):
        """ Saves the DataFrame as a CSV file. """
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        df.to_csv(self.filepath, index=False)
        print(f"✅ Data saved to {self.filepath}")

    def run(self):
        """ Runs the scraper: fetch data, process it, and save. """
        data = self.fetch_html_table(self.URL)  # Fetch HTML table
        if data is not None:
            df = self.process_data(data)
            if df is not None:
                self.save_to_csv(df)
