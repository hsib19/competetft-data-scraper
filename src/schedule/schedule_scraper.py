from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import time
import json
from pathlib import Path
from src.config.settings import SCHEDULE_URL
from src.utils.logger import logger

# Directory to save raw scraped data
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = RAW_DATA_DIR / "schedule.json"


def scrape(retries=3, delay=5):
    """
    Scrape the tournaments schedule from CompetetFT.
    
    Returns:
        list of dicts: Each dict contains 'date' and 'tournaments' (list of tournament info)
        
    Side-effect:
        Saves the scraped data to data/raw/schedule.json
    """
    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"[Schedule Scraper] Attempt {attempt + 1}")
            
            # Launch a headless Chromium browser
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Capture page console logs and forward to our logger
                page.on("console", lambda msg: logger.info(f"[PAGE LOG] {msg.text}"))

                # Navigate to schedule page and wait for DOM content to load
                page.goto(SCHEDULE_URL, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)  # Wait a bit for JavaScript to render

                # Execute JS in page context to scrape tournaments
                data = page.evaluate("""
                    () => {
                        const result = []
                        // Select all sections that have data-date attribute
                        const sections = Array.from(document.querySelectorAll('section[data-date]'))
                        sections.forEach(section => {
                            const date_label = section.getAttribute('data-date')
                            let p1 = section.nextElementSibling
                            const tournaments = []

                            // Only proceed if the next element contains tournaments
                            if (p1 && p1.classList.contains('p_1')) {
                                Array.from(p1.children).forEach(child => {
                                    const a = child.querySelector('a[href*="/tournament/"]')
                                    if (a) {
                                        // Extract tournament time
                                        const timeEl = a.querySelector('time')
                                        const timeText = timeEl ? timeEl.textContent.trim() : 'none'

                                        // Extract tournament name
                                        const nameEl = a.querySelectorAll('div.ta_right')[0]
                                        const name = nameEl ? nameEl.textContent.trim() : 'none'

                                        // Extract status text
                                        const statusDiv = Array.from(a.querySelectorAll('div.ta_left')).find(d => d.textContent.trim() !== '')
                                        const status = statusDiv ? statusDiv.textContent.trim() : 'none'

                                        // Determine region from SVG fill color
                                        let region = 'unknown'
                                        const svgPath = a.querySelector('svg path')
                                        if (svgPath) {
                                            const fill = svgPath.getAttribute('fill')
                                            if (fill === '#5B23B5') region = 'APAC'
                                            else if (fill === '#3F34FF') region = 'AMER'
                                            else if (fill === '#FF6807') region = 'EMEA'
                                        }

                                        // Extract href and tournament_id from URL
                                        const href = a.getAttribute('href') || 'none'
                                        const tournament_id = href.split('/').pop() || 'none'

                                        // Push tournament info to tournaments array
                                        tournaments.push({
                                            'tournament_id': tournament_id,
                                            'href': href,
                                            'time': timeText,
                                            'name': name,
                                            'status': status,
                                            'region': region
                                        })
                                    }
                                })
                            }

                            // Push each date section with its tournaments
                            result.push({'date': date_label, 'tournaments': tournaments})
                        })
                        return result
                    }
                """)
                
                # Close browser
                browser.close()

                # Save scraped data to JSON
                with RAW_FILE.open("w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                logger.info(f"[Schedule Scraper] Success: {len(data)} sections scraped and saved to {RAW_FILE}")
                return data

        except PlaywrightTimeoutError as e:
            logger.warning(f"[Schedule Scraper] Timeout on attempt {attempt + 1}: {e}")
        except Exception as e:
            logger.error(f"[Schedule Scraper] Error on attempt {attempt + 1}: {e}")

        attempt += 1
        time.sleep(delay)

    # If all retries failed
    logger.error("[Schedule Scraper] Failed to fetch after all retries")
    return []
