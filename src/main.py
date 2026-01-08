from events.events_scraper import scrape as scrape_events
from schedule.schedule_scraper import scrape as scrape_schedule
from tournament.tournament_scraper import scrape as scrape_tournaments
from tournament.participants_scraper import scrape as scrape_participants
from pro_points.pro_points_scraper import scrape as scrape_pro_points
from ladder_points.ladder_scraper import scrape as scrape_ladder_points

def main():
    print("Starting CompetetFT Scraper...")
    scrape_events()
    scrape_schedule()
    scrape_tournaments()
    scrape_participants()
    scrape_pro_points()
    scrape_ladder_points()
    print("Scraper finished.")

if __name__ == "__main__":
    main()
