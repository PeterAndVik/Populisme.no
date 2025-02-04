import sys
import os
import pandas as pd

# ✅ Ensure correct paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scrapers.base_scraper import BaseScraper

class PollScraper(BaseScraper):
    """
    Scraper for polling data from Poll of Polls.
    Inherits from BaseScraper and scrapes an HTML table.
    """
    URL = "https://www.pollofpolls.no/?cmd=Stortinget&do=visallesnitt"

    def __init__(self):
        # ✅ Tell `BaseScraper` to use HTML scraping (not API or CSV)
        super().__init__("poll_data_raw.csv", use_api=False, use_csv=False)

    def process_data(self, df):
        """
        ✅ Processes the polling data from HTML tables.
        """
        if df is None or df.empty:
            print("⚠️ No data was extracted from the HTML table.")
            return None

        # ✅ Rename the first column (assumed to be the month)
        df.rename(columns={'Unnamed: 0': 'Month'}, inplace=True)

        return df

if __name__ == "__main__":
    scraper = PollScraper()
    scraper.run()
