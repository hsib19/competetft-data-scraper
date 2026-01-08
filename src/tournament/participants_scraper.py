from .models import Participant
from utils.storage import save_json

def scrape():
    """Dummy scraping for participants."""
    print("Scraping participants (dummy)...")
    data = [
        Participant(id="p1", name="PlayerOne", rank=1).dict(),
        Participant(id="p2", name="PlayerTwo", rank=2).dict(),
    ]
    save_json(data, "participants.json")
    return data
