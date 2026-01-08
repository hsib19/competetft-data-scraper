from .models import ProPoint
from src.utils.storage import save_json

def scrape():
    """Dummy scraping for pro points."""
    print("Scraping pro points (dummy)...")
    data = [
        ProPoint(player_id="p1", points=120, rank=1).dict(),
        ProPoint(player_id="p2", points=110, rank=2).dict(),
    ]
    save_json(data, "pro_points.json")
    return data
