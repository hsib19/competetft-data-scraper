from .models import LadderPoint
from utils.storage import save_json

def scrape():
    """Dummy scraping for ladder points."""
    print("Scraping ladder points (dummy)...")
    data = [
        LadderPoint(player_id="p1", points=150, rank=1).dict(),
        LadderPoint(player_id="p2", points=140, rank=2).dict(),
    ]
    save_json(data, "ladder_points.json")
    return data
