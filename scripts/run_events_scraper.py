import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.events import scrape

if __name__ == "__main__":
    events = scrape()
    print(f"Scraped {len(events)} events")
