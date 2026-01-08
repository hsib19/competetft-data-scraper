from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import time
from pathlib import Path
import json
from src.config.settings import BASE_URL
from src.utils.logger import logger

# Directory to save raw scraped data
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = RAW_DATA_DIR / "events.json"

URL = f"{BASE_URL}/en-US/schedule"

def fetch_events_by_id(container_id, category, retries=3, delay=5):
    """
    Scrape events from a specific container on the schedule page.
    Args:
        container_id (str): The HTML id of the container
        category (str): Friendly name for logging
    Returns:
        list of dicts: Each dict has url, name, type, category, tournament_id
    """
    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"[Events Scraper] {category} ({container_id}) attempt {attempt+1}")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(URL, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)

                # Execute JS to scrape items
                items = page.evaluate(f"""
                () => {{
                    const container = document.querySelector('[id*="{container_id}"]');
                    if (!container) return [];
                    const as = Array.from(container.querySelectorAll('ol > li > a'));
                    return as.map(a => {{
                        const ps = a.querySelectorAll('div > p');
                        const name = ps[0] ? ps[0].textContent.trim() : 'unknown';
                        const type = ps[1] ? ps[1].textContent.trim().replace(/event/i, '').trim() : 'unknown';
                        const url = a.getAttribute('href') || '';
                        
                        // Extract tournament_id from url
                        const parts = url.split('/');
                        const tournament_id = parts.length > 0 ? parts[parts.length - 1] : 'unknown';
                        
                        return {{ url, tournament_id, name, type }};
                    }});
                }}
            """)

                browser.close()

                for e in items:
                    e['category'] = category

                return items

        except PlaywrightTimeoutError as e:
            logger.warning(f"[Events Scraper] Timeout on attempt {attempt+1} for {category}: {e}")
        except Exception as e:
            logger.error(f"[Events Scraper] Error on attempt {attempt+1} for {category}: {e}")

        attempt += 1
        time.sleep(delay)

    logger.error(f"[Events Scraper] Failed to fetch {category} after {retries} attempts")
    return []


def fetch_pro_circuit():
    """Fetch Pro Circuit events"""
    return fetch_events_by_id('r0', "Pro Circuit")


def fetch_path_to_pro():
    """Fetch Path to Pro events"""
    return fetch_events_by_id('r2', "Path to Pro")


def scrape():
    """
    Main entry point for events scraping.
    Combines Pro Circuit and Path to Pro, saves raw JSON, and returns list.
    """
    logger.info("[Events Scraper] Starting scrape...")

    pro_circuit = fetch_pro_circuit()
    path_to_pro = fetch_path_to_pro()

    all_events = pro_circuit + path_to_pro

    # Save raw JSON
    with RAW_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=4)

    logger.info(f"[Events Scraper] Finished. Scraped {len(all_events)} items, saved to {RAW_FILE}")

    return all_events
