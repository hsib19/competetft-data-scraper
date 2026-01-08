import sys
from pathlib import Path
from datetime import datetime

# Add the project root directory to the Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Import scraper, database session, and models
from src.schedule.schedule_scraper import scrape
from src.db.session import SessionLocal
from src.db.models import Schedule, TournamentSchedule

def save_schedule():
    # Scrape schedule data (expected as a list of dictionaries)
    schedules = scrape()
    session = SessionLocal()

    try:
        for s in schedules:
            # Parse date string into a Python date object
            date_obj = datetime.strptime(s["date"], "%Y-%m-%d").date()

            # Create and insert Schedule record first
            schedule = Schedule(date=date_obj)
            session.add(schedule)
            session.flush()  # Ensure schedule.id is immediately available

            for t in s["tournaments"]:
                # Check if the tournament already exists for this schedule
                existing = session.query(TournamentSchedule).filter_by(
                    schedule_id=schedule.id,
                    tournament_id=t["tournament_id"]
                ).first()

                if existing:
                    continue  # Skip duplicate tournaments

                # Create and insert TournamentSchedule record
                tournament = TournamentSchedule(
                    schedule_id=schedule.id,
                    tournament_id=t["tournament_id"],
                    url=t["url"],
                    time=t["time"],
                    name=t["name"],
                    region=t["region"],
                )
                session.add(tournament)

        # Commit all changes to the database
        session.commit()
        print(f"Inserted {len(schedules)} schedules with tournaments")

    except Exception as ex:
        # Roll back the transaction if any error occurs
        session.rollback()
        print("Error inserting schedule:", ex)
    finally:
        # Always close the database session
        session.close()

if __name__ == "__main__":
    # Execute the script when run directly
    save_schedule()
