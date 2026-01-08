from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pathlib import Path
import logging
import time
import json
from src.utils.logger import logger
from src.config.settings import BASE_URL 

# ===== Raw data storage setup =====
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = RAW_DATA_DIR / "pro_points.json"

# URL for the specific Pro Points page (season/tournament)
PRO_POINTS_URL = f"{BASE_URL}/en-US/season/115371820222511550/points/114777641829694521"

def scrape(retries=3, delay=5):
    """
    Scrape Pro Points page including:
      - Players table with rank, nickname, main_char, and cup totals
      - About Pro Points section
      - Pro Points Seeding section (description + list)
    
    Returns:
        dict: Contains 'players', 'about', 'seeding'
    Side-effect:
        Saves raw JSON to data/raw/pro_points.json
    """
    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"[Pro Points] Attempt {attempt + 1}")

            # ===== Launch headless browser =====
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Capture browser console logs
                page.on("console", lambda msg: logger.info(f"[PAGE LOG] {msg.text}"))
                
                # Navigate to the Pro Points URL and wait for page content
                page.goto(PRO_POINTS_URL, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)  # Allow JS to render table/content

                # ===== Evaluate JavaScript inside the page context =====
                data = page.evaluate("""
                    () => {
                        const result = {};

                        // ===== Players Table =====
                        const players = [];
                        const table = document.querySelector('table');
                        if (table) {
                            const rows = table.querySelectorAll('tbody tr');
                            rows.forEach(tr => {
                                const tds = tr.querySelectorAll('td');
                                if (tds.length < 3) return;  // skip invalid rows
                                const rank = parseInt(tds[0].textContent.trim());
                                const full = tds[1].textContent.trim();
                                let nickname = null;
                                let main_char = null;

                                // ===== Split nickname and main_char =====
                                if (full) {
                                    const lastSpace = full.lastIndexOf(' ');
                                    if (lastSpace === -1) {
                                        // Only one word, assign to both nickname and main_char
                                        nickname = full;
                                        main_char = full;
                                    } else {
                                        // Split by last space
                                        nickname = full.slice(0, lastSpace).trim();
                                        main_char = full.slice(lastSpace + 1).trim();

                                        // Fix case where main_char does not contain '#'
                                        if (!main_char.includes('#') && nickname.includes('#')) {
                                            // Extract substring containing '#' as main_char
                                            const hashIndex = nickname.indexOf('#');
                                            main_char = nickname.slice(hashIndex - nickname.slice(0, hashIndex).lastIndexOf(' ')).trim();
                                            nickname = full.replace(main_char, '').trim();
                                        }
                                    }
                                }

                                // ===== Parse point totals =====
                                const total_points = parseInt(tds[2].textContent.trim());
                                const demacia_cup_total = parseInt(tds[3].textContent.trim());
                                const bilgewater_cup_total = parseInt(tds[4].textContent.trim());
                                const shurima_cup_total = parseInt(tds[5].textContent.trim());

                                // Push player object to list
                                players.push({
                                    rank,
                                    nickname,
                                    main_char,
                                    total_points,
                                    demacia_cup_total,
                                    bilgewater_cup_total,
                                    shurima_cup_total
                                });
                            });
                        }
                        result.players = players;

                        // ===== About Pro Points Section =====
                        let about = null;
                        const h5s = Array.from(document.querySelectorAll('h5'));
                        const aboutH5 = h5s.find(h => h.textContent.trim() === "About Pro Points");
                        if (aboutH5 && aboutH5.nextElementSibling && aboutH5.nextElementSibling.tagName === 'P') {
                            about = aboutH5.nextElementSibling.textContent.trim();
                        }
                        result.about = about;

                        // ===== Pro Points Seeding Section =====
                        let seeding = { description: null, list: [] };

                        // Find h5 element with text "Pro Points Seeding"
                        const seedingH5 = h5s.find(h => h?.textContent?.trim() === 'Pro Points Seeding');

                        if (seedingH5) {
                            // Grab the paragraph below h5 for description
                            const descP = seedingH5.nextElementSibling;
                            if (descP?.tagName === 'P') {
                                seeding.description = descP.textContent.trim();

                                // Skip <hr> elements to find the <ul>
                                let ul = descP.nextElementSibling;
                                while (ul && ul.tagName !== 'UL') {
                                    ul = ul.nextElementSibling;
                                }

                                // Parse each <li> in the <ul>
                                if (ul?.tagName === 'UL') {
                                    Array.from(ul.querySelectorAll('li')).forEach(li => {
                                        if (!li) return;

                                        const divs = Array.from(li.querySelectorAll('div') || []);

                                        // First div = title
                                        const title = divs[0]?.textContent?.trim() || null;

                                        // Second div > p = description
                                        let desc = null;
                                        const innerDiv = divs[1];
                                        if (innerDiv) {
                                            const p = innerDiv.querySelector('p');
                                            if (p) desc = p.textContent.trim();
                                        }

                                        seeding.list.push({ title, desc });
                                    });
                                }
                            }
                        }

                        result.seeding = seeding;

                        return result;
                    }
                """)
                browser.close()

                # ===== Add metadata =====
                for d in data["players"]:
                    d["tournament_id"] = "114777641829694521"
                    d["url"] = PRO_POINTS_URL

                # ===== Save raw JSON =====
                with RAW_FILE.open("w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                logger.info(f"[Pro Points] Scraped {len(data['players'])} players, saved to {RAW_FILE}")
                return data

        except TimeoutError as e:
            logger.warning(f"[Pro Points] Timeout on attempt {attempt + 1}: {e}")
        except Exception as e:
            logger.error(f"[Pro Points] Error on attempt {attempt + 1}: {e}")

        attempt += 1
        time.sleep(delay)

    logger.error("[Pro Points] Failed to scrape after all retries")
    return {}
