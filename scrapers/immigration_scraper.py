import sys
import os
import pandas as pd

# ✅ Ensure correct paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scrapers.base_scraper import BaseScraper

class ImmigrationScraper(BaseScraper):
    """
    Scraper for Norwegian immigration statistics from SSB.
    """
    URL = "https://data.ssb.no/api/v0/dataset/48670.csv?lang=no"

    def __init__(self):
        # ✅ Now using `use_csv=True` to enable CSV scraping
        super().__init__("immigration_raw.csv", use_api=False, use_csv=True)

    def process_data(self, df):
        """
        ✅ Processes the CSV data before saving.
        """
        df = df.rename(columns={
            "07108: Innvandrere og norskfødte med innvandrerforeldre, etter region, kjønn, landbakgrunn, år og statistikkvariabel": "Innvandring"
        })
        return df

if __name__ == "__main__":
    scraper = ImmigrationScraper()
    scraper.run()
