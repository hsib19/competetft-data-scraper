import asyncio
from src.events.events_scraper import scrape as scrape_events
from src.schedule.schedule_scraper import scrape as scrape_schedule
from src.tournament.tournament_scraper import scrape as scrape_tournaments
from src.pro_points.pro_points_scraper import scrape as scrape_pro_points
from src.ladder_points.ladder_scraper import scrape as scrape_ladder_points
from src.utils.logger import logger

async def main():
    logger.info("Starting CompetetFT Scraper...")

    # Scrape events
    events = await asyncio.to_thread(scrape_events)

    # Scrape schedule
    schedule = await asyncio.to_thread(scrape_schedule)

    # Manually test 1 tournament ID
    tournament_ids = ["115372050843537506"]  
    logger.info(f"Testing tournament scrape with ID: {tournament_ids[0]}")

    # Scrape tournament details + participants
    tournaments = await asyncio.to_thread(scrape_tournaments, tournament_ids)

    # Scrape pro points and ladder points
    pro_points = await asyncio.to_thread(scrape_pro_points)
    ladder_points = await asyncio.to_thread(scrape_ladder_points)

    # Logging results
    logger.info("All scraper modules finished.")
    logger.info(f"Events scraped: {len(events)}")
    logger.info(f"Schedule sections: {len(schedule)}")
    logger.info(f"Tournaments scraped: {len(tournaments)}")
    logger.info(f"Pro points entries: {len(pro_points)}")
    logger.info(f"Ladder points entries: {len(ladder_points)}")

if __name__ == "__main__":
    asyncio.run(main())
