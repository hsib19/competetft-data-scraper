from src.events.models import EventItem
from src.db.insert import insert_event

def process_events(raw_events):
    """
    Validate and insert scraped events into DB.
    """
    inserted_ids = []
    for raw in raw_events:
        try:
            event = EventItem(**raw)   # validate with Pydantic
            inserted_id = insert_event(event)
            inserted_ids.append(inserted_id)
        except Exception as err:
            print(f"[events] Skipped due to error: {err}")
    return inserted_ids
