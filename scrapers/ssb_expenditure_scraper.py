import sys
import os

# Legger til prosjektets rotmappe i sys.path slik at scrapers kan importeres riktig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scrapers.base_scraper import BaseScraper
import pandas as pd

class SSBExpenditureScraper(BaseScraper):
    """
    Skraper offentlige utgifter fra SSBs API.
    """
    URL = "https://data.ssb.no/api/v0/no/table/10487/"

    # Genererer årstall automatisk
    START_YEAR = 2014
    END_YEAR = 2025
    YEARS = [str(year) for year in range(START_YEAR, END_YEAR + 1)]

    PAYLOAD = {
        "query": [
            {
                "code": "Hovedpost",
                "selection": {"filter": "item", "values": ["UTG.IALT"]}
            },
            {
                "code": "Tid",
                "selection": {"filter": "item", "values": YEARS}
            }
        ],
        "response": {"format": "json-stat2"}
    }

    def __init__(self):
        super().__init__("ssb_expenditure_raw.csv", use_api=True)  # ✅ Tell BaseScraper this is an API scraper

    def process_data(self, data):
        """ Konverterer JSON til en DataFrame. """
        time_periods = data["dimension"]["Tid"]["category"]["label"]
        values = data["value"]
        return pd.DataFrame({"Year": list(time_periods.values()), "Total Expenditure (mill. kr)": values})

if __name__ == "__main__":
    scraper = SSBExpenditureScraper()
    scraper.run()
