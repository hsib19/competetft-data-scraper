import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.db.session import SessionLocal
from src.db.models import ProPointsPlayer, ProPointsSeeding, ProPointsMeta
from src.pro_points.pro_points_scraper import scrape

def save_pro_points():
    data = scrape()
    session = SessionLocal()

    try:
        # Insert players
        for p in data.get("players", []):
            player = ProPointsPlayer(
                rank=p["rank"],
                nickname=p["nickname"],
                main_char=p["main_char"],
                total_points=p["total_points"],
                demacia_cup_total=p["demacia_cup_total"],
                bilgewater_cup_total=p["bilgewater_cup_total"],
                shurima_cup_total=p["shurima_cup_total"],
                tournament_id=p["tournament_id"],
                url=p["url"],
            )
            session.add(player)

        # Insert seeding rules
        for s in data.get("seeding", {}).get("list", []):
            seeding = ProPointsSeeding(
                title=s["title"],
                description=s["desc"],
            )
            session.add(seeding)

        # Insert meta info
        meta = ProPointsMeta(
            about=data.get("about"),
            seeding_description=data.get("seeding", {}).get("description"),
        )
        session.add(meta)

        session.commit()
        print(f"Inserted {len(data.get('players', []))} players, "
              f"{len(data.get('seeding', {}).get('list', []))} seeding rules, "
              f"and meta info")

    except Exception as ex:
        session.rollback()
        print("Error inserting pro points:", ex)
    finally:
        session.close()

if __name__ == "__main__":
    save_pro_points()
