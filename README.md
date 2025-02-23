# 📌 Updated README for Populisme.no

This guide explains you need to add a new scraper and processing script.
It includes detailed explanations and step-by-step instructions to avoid confusion.

## 📌 Table of Contents

- Project Structure
- How to Add a New Scraper
  - Understanding the Scraper Template
- How to Add a New Data Processing Script
  - Understanding the Processing Script Template
- Automation: Running All Scrapers
- Troubleshooting

## 📌 Project Structure

The project is organized into clear folders:

```
Populisme.no/
│
├── automation/                   # Automates scraping and processing
│   ├── run_pipeline.py           # Runs all scrapers automatically
│    ├── update_graphs.json        # Updates list of graphs on flere grafer 
│
├── scrapers/                      # Scrapers to collect data
│   ├── ssb_expenditure_scraper.py # scraper (SSB)
│   ├── poll_scraper.py            # scraper (Polls)
│   ├── immigration_scraper.py     # scraper (innvandring)
│
├── data/                          
│   ├── raw/                        # Raw scraped data (CSV)
│   ├── processed/                  # Cleaned data (CSV)
│
├── data_processing/                    # Data cleaning & visualization
│   ├── process_ssb_expenditures.py     # Cleans & graphs SSB expenditure
│   ├── process_poll_data.py            # Cleans & graphs poll data
│   ├── process_aggregated_poll_data.py # Aggregates poll data & graphs
│   ├── process_immigration_data.py     # Cleans & graphs immigration data
│
├── utils/                      # Scrapers to collect data
│   ├── __init__.py                # Makes this folder a package
│   ├── base_scraper.py            # The main scraper template
│   ├── graph_utils.py             # used to make all graphs in same style
│
├── graphs/                         # Saved HTML graphs
│
├── static/                         # Website assets (CSS, JS)
│
├── index.html                      # Main webpage
├── flere_grafer.html               # Page for additional graphs
│
└── README.md                       # 📌 YOU ARE HERE! 🎉
```

## 📌 How to Add a New Scraper
If you want to scrape new data, follow these steps.

### **1️⃣ Create a New Scraper File**
- Go to `scrapers/`
- Create a new Python file (e.g., `my_new_scraper.py`).

### **2️⃣ Use the Correct Scraper Type**
`BaseScraper` now supports **three types** of scrapers:
1. **API Scrapers** → Use `use_api=True`
2. **HTML Table Scrapers** → Use `use_api=False, use_csv=False`
3. **CSV Scrapers** → Use `use_api=False, use_csv=True`

Copy this into your new scraper file (`scrapers/my_new_scraper.py`) and read the comments carefully:

```python
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.base_scraper import BaseScraper

class MyNewScraper(BaseScraper):
    """
    Scraper for [INSERT DATA SOURCE HERE].
    (What and where the scraper scrapes with text)
    """

    URL = "https://example.com/api"  # CHANGE THIS
    PAYLOAD = {}  # CHANGE THIS IF USING AN API

    def __init__(self):
        super().__init__("my_new_scraper_raw.csv", use_api=True)  # ✅ CHANGE THE FILE NAME AND SCRAPER TYPE

    def process_data(self, data):
        df = pd.DataFrame(data)  # MODIFY THIS BASED ON DATA STRUCTURE
        return df

if __name__ == "__main__":
    scraper = MyNewScraper()
    scraper.run()
```

### 3️⃣ Run the Scraper

After making changes, run the scraper manually to check if it works:

```sh
python scrapers/my_new_scraper.py
```

✅ If successful, it should create a file in `data/raw/`.

## 📌 How to Add a New Data Processing Script (Step by Step)

After adding a scraper, you need to clean the data and generate graphs.

### 1️⃣ Create a New Processing File

- Go to `data_processing/`
- Create a new Python file (e.g., `process_my_new_scraper.py`).

### 2️⃣ Use the Processing Script Template

Copy this into your new processing file (`data_processing/process_my_new_scraper.py`) and follow the instructions:

```python
import os
import pandas as pd
import plotly.express as px

RAW_FILE = "data/raw/my_new_scraper_raw.csv"
PROCESSED_FILE = "data/processed/my_new_scraper_clean.csv"
GRAPH_HTML_FILE = "graphs/my_new_scraper.html"

if not os.path.exists(RAW_FILE):
    print(f"⚠️ Raw file not found: {RAW_FILE}")
    exit()

df = pd.read_csv(RAW_FILE)
df.dropna(inplace=True)  # Example: Remove empty rows

os.makedirs("data/processed", exist_ok=True)
df.to_csv(PROCESSED_FILE, index=False)
print(f"✅ Cleaned data saved: {PROCESSED_FILE}")

fig = px.line(df, x="Date", y="Value", title="My New Data Over Time")
os.makedirs("graphs", exist_ok=True)
fig.write_html(GRAPH_HTML_FILE)
print(f"📊 Graph saved as HTML: {GRAPH_HTML_FILE}")
fig.show()
```

## 📌 Automation: Running All Scrapers
(work in progress)

To run all scrapers at once, use:

```sh
python automation/run_pipeline.py
```

🚀 This will fetch data for all scrapers and save raw CSVs in `data/raw/`.

## 📌 Troubleshooting (add more troubleshooting solutions if you find them here)

**"ModuleNotFoundError: No module named 'scrapers'"**

✅ Solution: Add this at the top of your script:

```python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
```

🚀 Now You’re Ready to Contribute!

🎉 Adding new scrapers and processing scripts is now possible!
Follow the guide, and you can scrape, clean, and visualize new data without breaking anything. 🚀
