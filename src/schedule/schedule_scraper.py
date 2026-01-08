from .models import ScheduleItem
from utils.storage import save_json

def scrape():
    """Dummy scraping for schedule."""
    print("Scraping schedule (dummy)...")
    data = [
        ScheduleItem(event_id="1", date="2026-01-01", match_url="https://example.com/match/1").dict(),
        ScheduleItem(event_id="2", date="2026-02-10", match_url="https://example.com/match/2").dict(),
    ]
    save_json(data, "schedule.json")
    return data
