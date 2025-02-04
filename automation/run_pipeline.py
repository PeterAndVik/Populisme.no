import os
import sys
import importlib.util

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SCRAPER_DIR = "scrapers"
PROCESSING_DIR = "data_processing"
UPDATE_GRAPHS_SCRIPT = "automation/update_graphs_json.py"  # ✅ This will be run at the end

def run_scripts_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "base_scraper.py":
            module_name = filename[:-3]  
            module_path = os.path.join(directory, filename)

            print(f"🚀 Running {module_name}...")
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"✅ Finished {module_name}.\n")

if __name__ == "__main__":
    print("📌 Running all scrapers...\n")
    run_scripts_from_directory(SCRAPER_DIR)

    print("📌 Running all data processing scripts...\n")
    run_scripts_from_directory(PROCESSING_DIR)

    print("📌 Updating graphs.json...\n")
    os.system(f"python {UPDATE_GRAPHS_SCRIPT}")  # ✅ Runs the script automatically

    print("🎉 All scraping, processing, and graph updates completed successfully!")
