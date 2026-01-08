import sys
from pathlib import Path

# Add the project's root directory to the Python path for module imports
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Import the scraper and database modules
from src.events import scrape
from src.db.session import SessionLocal
from src.db.models import Event

def save_events():
    # Get the list of events from the scraper
    events = scrape()
    session = SessionLocal()

    try:
        for e in events:
            # Check if the tournament_id already exists in the database
            existing = session.query(Event).filter_by(tournament_id=e["tournament_id"]).first()
            if existing:
                continue  # Skip duplicate entries

            # Create a new Event object
            event = Event(
                tournament_id=e["tournament_id"],
                url=e["url"],
                name=e["name"],
                type=e["type"],
                category=e["category"],
            )
            # Add the new event to the session
            session.add(event)

        # Commit all changes to the database
        session.commit()
        print(f"Inserted {len(events)} events into DB")
    except Exception as ex:
        # Rollback the session if any error occurs
        session.rollback()
        print("Error inserting events:", ex)
    finally:
        # Close the database session
        session.close()

if __name__ == "__main__":
    # Run the save_events function when this script is executed
    save_events()
