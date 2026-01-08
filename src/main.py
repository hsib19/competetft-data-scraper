import asyncio
from events.events_scraper import scrape as scrape_events
from schedule.schedule_scraper import scrape as scrape_schedule
from tournament.tournament_scraper import scrape as scrape_tournaments
from tournament.participants_scraper import scrape as scrape_participants
from pro_points.pro_points_scraper import scrape as scrape_pro_points
from ladder_points.ladder_scraper import scrape as scrape_ladder_points
from utils.logger import logger

async def main():
    logger.info("Starting CompetetFT Scraper...")

    # Run a;; scraper async
    tasks = [
        asyncio.to_thread(scrape_events),
        asyncio.to_thread(scrape_schedule),
        asyncio.to_thread(scrape_tournaments),
        asyncio.to_thread(scrape_participants),
        asyncio.to_thread(scrape_pro_points),
        asyncio.to_thread(scrape_ladder_points)
    ]

    results = await asyncio.gather(*tasks)
    
    logger.info("All scraper modules finished.")
    logger.info("Results summary:")
    for res in results:
        logger.info(f" - {len(res)} items scraped")

if __name__ == "__main__":
    asyncio.run(main())
