import sys
import os

# Legger til prosjektets rotmappe i sys.path slik at scrapers kan importeres riktig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from scrapers.base_scraper import BaseScraper

class PollScraper(BaseScraper):
    """
    Scraper for polling data from Poll of Polls.
    Inherits from BaseScraper and scrapes an HTML table.
    """
    URL = "https://www.pollofpolls.no/?cmd=Stortinget&do=visallesnitt"

    def __init__(self):
        super().__init__("poll_data_raw.csv")

    def process_data(self, df):
        """ Prepares the poll data for saving (no major cleaning yet). """
        # Rename the first column (assumed to be the month)
        df.rename(columns={'Unnamed: 0': 'Month'}, inplace=True)
        return df

if __name__ == "__main__":
    scraper = PollScraper()
    scraper.run()
