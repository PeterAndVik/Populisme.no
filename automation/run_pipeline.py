import os
import sys
import importlib.util

# ✅ Ensure correct paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Paths to scrapers and processing scripts
SCRAPER_DIR = "scrapers"
PROCESSING_DIR = "data_processing"

def run_scripts_from_directory(directory):
    """
    Dynamically finds and runs all Python scripts in the given directory.
    - Works for both `scrapers/` and `data_processing/`
    """
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "base_scraper.py":  # ✅ Exclude `base_scraper.py`
            module_name = filename[:-3]  # Remove `.py` extension
            module_path = os.path.join(directory, filename)

            print(f"🚀 Running {module_name}...")

            # Load and execute the script dynamically
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print(f"✅ Finished {module_name}.\n")

if __name__ == "__main__":
    print("📌 Running all scrapers...\n")
    run_scripts_from_directory(SCRAPER_DIR)

    print("📌 Running all data processing scripts...\n")
    run_scripts_from_directory(PROCESSING_DIR)

    print("🎉 All scraping and processing completed successfully!")
