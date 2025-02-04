import os
import json

# ✅ Define the graphs directory and JSON file path
GRAPHS_DIR = "graphs"
JSON_FILE = os.path.join(GRAPHS_DIR, "graphs.json")

def update_graphs_json():
    """
    Automatically updates `graphs.json` with the latest graphs in the `graphs/` folder.
    """
    # ✅ Get all `.html` files in the `graphs/` directory
    graph_files = [f for f in os.listdir(GRAPHS_DIR) if f.endswith(".html")]

    # ✅ Create JSON structure
    graphs_data = {"graphs": graph_files}

    # ✅ Save updated `graphs.json`
    with open(JSON_FILE, "w") as json_file:
        json.dump(graphs_data, json_file, indent=4)

    print(f"✅ Updated {JSON_FILE} with {len(graph_files)} graphs.")

if __name__ == "__main__":
    update_graphs_json()
