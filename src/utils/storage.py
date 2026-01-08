import json
import os
from src.config.settings import DATA_DIR

os.makedirs(DATA_DIR, exist_ok=True)

def save_json(data, filename):
    """Save data to JSON file in data/ folder."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved data to {filepath}")
