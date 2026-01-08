from src.db.session import SessionLocal
from src.db.models import Event

def insert_event(event_item):
    """
    Insert a validated EventItem into the DB.
    """
    session = SessionLocal()
    try:
        record = Event(
            tournament_id=event_item.tournament_id,
            url=event_item.url,
            name=event_item.name,
            type=event_item.type,
            category=event_item.category,
        )
        session.add(record)
        session.commit()
        return record.tournament_id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
