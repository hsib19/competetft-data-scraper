from .models import Event
from src.utils.storage import save_json

def scrape():
    """Dummy scraping for events."""
    print("Scraping events (dummy)...")
    data = [
        Event(id="1", name="Winter Championship", start_date="2026-01-01", end_date="2026-01-05").dict(),
        Event(id="2", name="Spring Showdown", start_date="2026-02-10", end_date="2026-02-15").dict(),
    ]
    save_json(data, "events.json")
    return data
