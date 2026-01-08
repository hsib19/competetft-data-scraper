from .models import Participants
from src.utils.storage import save_json

def scrape():
    """Dummy scraping for participants (nickname list only)."""
    print("Scraping participants (dummy)...")
    data = Participants(
        tournament_id="115372050843537506",
        url="https://competetft.com/en-US/tournament/115372050843537506/participants",
        participants=[
            "SheeepStick", "Lilbear", "Yeso", "Tamama", "mori", "seoill",
            "T1 sCsC", "Grenade", "Asta1", "steppy", "FW AQ1H", "FW Kbaobao",
            "FW Iron Bog", "KAITO", "ZETA yatsuhashi", "WithoutYou", "oubo",
            "Inpath", "Carpe Diem", "Maladjust", "tristan", "Jazlatte",
            "VP Maris", "VP Milo", "yesports terry", "ZETA title",
            "ZETA summertimer", "ROC Dr OH", "ROC Ssangyeop", "FN Ssiel",
            "T1 Binteum", "YBY1"
        ]
    ).dict()

    save_json(data, "participants.json")
    return data
