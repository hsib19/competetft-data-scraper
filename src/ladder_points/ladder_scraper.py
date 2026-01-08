from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pathlib import Path
import logging
import time
import json
from src.utils.logger import logger
from src.config.settings import BASE_URL

# ===== Raw data folder =====
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = RAW_DATA_DIR / "ladder_points.json"

# URL for Ladder Points page
LADDER_URL = f"{BASE_URL}/en-US/ladder-points/115376765699628532?shard=SG2"

def scrape(retries=3, delay=5):
    """
    Scrape Ladder Points page including:
      - Updated / Next Update timestamps
      - Players table with total and per-week points
    Side-effect:
      Saves raw JSON to data/raw/ladder_points.json
    """
    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"[Ladder Points] Attempt {attempt + 1}")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Capture browser console logs
                page.on("console", lambda msg: logger.info(f"[PAGE LOG] {msg.text}"))
                
                # Navigate to Ladder Points URL
                page.goto(LADDER_URL, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)

                # ===== Evaluate JS in page =====
                data = page.evaluate("""
                () => {
                    const result = {};

                    // ===== Updated / Next Update =====
                    const updateP = Array.from(document.querySelectorAll('p'))
                        .find(p => p.querySelector('span') && p.querySelector('span').textContent.includes('Updated'));
                    const nextUpdateP = Array.from(document.querySelectorAll('p'))
                        .find(p => p.querySelector('span') && p.querySelector('span').textContent.includes('Next Update'));

                    if (updateP) {
                        // Split by colon and trim to get the update timestamp
                        result.updated = updateP.textContent.split(':')[1].trim();
                    }

                    if (nextUpdateP) {
                        // Split by colon and trim to get the next update timestamp
                        result.next_update = nextUpdateP.textContent.split(':')[1].trim();
                    }

                    // ===== Players Table =====
                    const table = document.querySelector('table');
                    const players = [];
                    const headers = [];

                    if (table) {
                        // Grab header titles
                        const ths = table.querySelectorAll('thead th');
                        ths.forEach(th => headers.push(th.textContent.trim()));

                        // Grab player rows
                        const rows = table.querySelectorAll('tbody tr');
                        rows.forEach(tr => {
                            const tds = tr.querySelectorAll('td');
                            if (tds.length < 3) return;

                            const rank = parseInt(tds[0].textContent.trim());       // first td = rank
                            const participant = tds[1].textContent.trim();          // second td = participant name

                            const points = {};
                            for (let i = 2; i < tds.length; i++) {                  // remaining tds = points
                                points[headers[i]] = tds[i].textContent.trim();
                            }

                            players.push({ rank, participant, points });
                        });
                    }

                    result.headers = headers;
                    result.players = players;

                    // ===== Ladder Points Seeding =====
                    const seeding = { description: null, list: [] };
                    const h4s = Array.from(document.querySelectorAll('h4'));
                    const seedingH4 = h4s.find(h => h.textContent.trim() === "Seeding in Regional Finals");

                    if (seedingH4) {
                        // Description = next div after h4
                        const descDiv = seedingH4.nextElementSibling;
                        if (descDiv) seeding.description = descDiv.textContent.trim();

                        // Find the <hr> following the description
                        let hr = descDiv.nextElementSibling;
                        while (hr && hr.tagName !== 'HR') hr = hr.nextElementSibling;

                        if (hr) {
                            // The container div after hr has all shard info
                            let ulContainer = hr.nextElementSibling;
                            if (ulContainer) {
                                const shards = ulContainer.querySelectorAll('div.d_flex.flex-d_column.gap_8');
                                shards.forEach(shardDiv => {
                                    const shardName = shardDiv.querySelector('p')?.textContent?.trim() || null;
                                    const week1 = shardDiv.querySelectorAll('div')[0]?.textContent?.trim() || null;
                                    const playIns = shardDiv.querySelectorAll('div')[1]?.textContent?.trim() || null;
                                    seeding.list.push({
                                        shard: shardName,
                                        week1,
                                        play_ins: playIns
                                    });
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
                for p in data["players"]:
                    p["url"] = LADDER_URL

                # ===== Save raw JSON =====
                with RAW_FILE.open("w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                logger.info(f"[Ladder Points] Scraped {len(data['players'])} players, saved to {RAW_FILE}")
                return data

        except TimeoutError as e:
            logger.warning(f"[Ladder Points] Timeout on attempt {attempt + 1}: {e}")
        except Exception as e:
            logger.error(f"[Ladder Points] Error on attempt {attempt + 1}: {e}")

        attempt += 1
        time.sleep(delay)

    logger.error("[Ladder Points] Failed to scrape after all retries")
    return {}
