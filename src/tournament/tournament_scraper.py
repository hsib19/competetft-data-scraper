import logging
from .tournament_detail import fetch_tournament_detail, fetch_tournament_participants

def scrape(tournament_ids):
    """
    Scrape tournament details and participants for a list of tournament IDs.
    Returns a list of dictionaries containing full tournament info.
    """
    results = []

    for tid in tournament_ids:
        logging.info(f"Scraping tournament {tid}")

        # Fetch tournament detail
        detail = fetch_tournament_detail(tid)
        if detail is None:
            logging.warning(f"Skipping tournament {tid}, failed to fetch details")
            continue

        # Fetch participants
        participants = fetch_tournament_participants(tid)
        if participants is not None:
            detail["participants"] = participants.get("participants", [])

        results.append(detail)

    return results
