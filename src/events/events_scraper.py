from .models import Event
from utils.storage import save_json

def scrape():
    print("Scraping events...")
    # TODO: implement scraping logic
    data = [
        Event(id="1", name="Example Event", start_date="2026-01-01", end_date="2026-01-05").dict()
    ]
    save_json(data, "events.json")
    return data
