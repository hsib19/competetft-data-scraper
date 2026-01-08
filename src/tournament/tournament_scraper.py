from .models import Tournament
from utils.storage import save_json

def scrape():
    """Dummy scraping for tournaments."""
    print("Scraping tournaments (dummy)...")
    data = [
        Tournament(id="1", name="Winter Cup", date="2026-01-05").dict(),
        Tournament(id="2", name="Spring Cup", date="2026-02-15").dict(),
    ]
    save_json(data, "tournaments.json")
    return data
