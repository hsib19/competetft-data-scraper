from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import time
import json
from pathlib import Path
from zoneinfo import ZoneInfo
from src.config.settings import BASE_URL
from src.utils.logger import logger

LOCAL_TZ = ZoneInfo("Asia/Jakarta")

# Directory to save raw tournament data
RAW_DATA_DIR = Path("data/raw/tournaments")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_tournament_detail(tournament_id, retries=3):
    """
    Fetch tournament detail from competetft.com
    Returns dict with overview, rules, placements, points allocation, etc.
    Saves JSON to data/raw/tournaments/{tournament_id}.json
    """
    url = f"{BASE_URL}/en-US/tournament/{tournament_id}/overview"
    file_path = RAW_DATA_DIR / f"{tournament_id}.json"

    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[Tournament] Fetch detail {tournament_id} attempt {attempt}")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)

                data = page.evaluate("""
                () => {

                
                    const result = {}

                    // ===== NAME =====
                    const title = document.querySelector('.grid-area_title h2')
                    result.name = title ? title.textContent.trim() : null

                    // ===== OVERVIEW, STREAM, RULES =====
                    let overview = null
                    let stream_url = null
                    let rules = []

                    const h5 = document.querySelector('h5')
                    if (h5) {
                        const p1 = h5.nextElementSibling
                        const p2 = p1 ? p1.nextElementSibling : null
                        const hr = p2 ? p2.nextElementSibling : null

                        // overview
                        if (p1 && p1.tagName === 'P') {
                            overview = p1.textContent.trim()
                        }

                        // stream link
                        if (p2 && p2.tagName === 'P') {
                            const match = p2.textContent.match(/https?:\/\/\S+/)
                            if (match) stream_url = match[0]
                        }

                        // ===== RULES =====

                        if (hr && hr.tagName === 'HR') {
                            let el = hr.nextElementSibling

                            while (el) {
                                const h6 = el.querySelector?.('h6')
                                if (h6) {
                                    const title = h6.textContent.trim()
                                    let points = []

                                    // struktur: h6 -> div -> ul -> li
                                    const containerDiv = h6.nextElementSibling
                                    if (containerDiv) {
                                        const ul = containerDiv.querySelector('ul')
                                        if (ul) {
                                            points = Array.from(ul.querySelectorAll('li'))
                                                .map(li => li.textContent.trim())
                                                .filter(Boolean)
                                        }
                                    }

                                    rules.push({ title, points })
                                }

                                el = el.nextElementSibling
                            }
                        }

                        result.rules = rules

                    }

                    result.overview = overview
                    result.stream_url = stream_url
                    result.rules = rules


                    // ===== STATUS =====
                    let status = null

                    const statusEl = document.querySelector(
                        '.grid-area_title > div > div:nth-child(1)'
                    )

                    if (statusEl) {
                        status = statusEl.textContent.trim()
                    }

                    result.status = status

                    // ===== TYPE =====
                    const typeEl = Array.from(document.querySelectorAll('p'))
                        .find(p => /regional|international|open/i.test(p.textContent))
                    result.type = typeEl ? typeEl.textContent.trim() : null

                    // ===== START & END DATE =====
                    let start_date = null
                    let end_date = null

                    const dateEl = document.querySelector(
                        '.grid-area_title > div > div:nth-child(2)'
                    )

                    if (dateEl) {
                        const raw = dateEl.textContent
                            .replace(/\u2009/g, ' ')
                            .replace(/\s+/g, ' ')
                            .trim()

                        const MONTHS = {
                            Jan: 1, Feb: 2, Mar: 3, Apr: 4,
                            May: 5, Jun: 6, Jul: 7, Aug: 8,
                            Sep: 9, Oct: 10, Nov: 11, Dec: 12
                        }

                        // Jan 9 – 11  OR  Jan 30 – Feb 2
                        const rangeMatch = raw.match(
                            /^([A-Za-z]+)\s+(\d+)\s*[–-]\s*(?:(\d+)|([A-Za-z]+)\s+(\d+))$/
                        )

                        if (rangeMatch) {
                            const year = new Date().getFullYear()

                            const startMonth = MONTHS[rangeMatch[1]]
                            const startDay = parseInt(rangeMatch[2], 10)

                            let endMonth = startMonth
                            let endDay

                            if (rangeMatch[3]) {
                                // Jan 9 – 11
                                endDay = parseInt(rangeMatch[3], 10)
                            } else {
                                // Jan 30 – Feb 2
                                endMonth = MONTHS[rangeMatch[4]]
                                endDay = parseInt(rangeMatch[5], 10)
                            }

                            start_date = `${year}-${String(startMonth).padStart(2, '0')}-${String(startDay).padStart(2, '0')}`
                            end_date = `${year}-${String(endMonth).padStart(2, '0')}-${String(endDay).padStart(2, '0')}`
                        }

                    }

                    result.start_date = start_date
                    result.end_date = end_date


                   // ===== REGION =====
                    let region = null

                    const regionEl = document.querySelector('.grid-area_title span')
                    if (regionEl) {
                        region = regionEl.textContent.trim()
                    }

                    result.region = region

                    // ===== PLACEMENTS & PRIZES =====
let placements_prizes = {
    description: null,
    items: []
}

const h5s = Array.from(document.querySelectorAll('h5'))
const ppTitle = h5s.find(h =>
    h.textContent.trim().toLowerCase() === 'placements & prizes'
)

if (ppTitle) {
    let el = ppTitle.nextElementSibling

    // cari hr
    while (el && el.tagName !== 'HR') {
        el = el.nextElementSibling
    }

    // deskripsi
    if (el?.nextElementSibling?.tagName === 'P') {
        placements_prizes.description =
            el.nextElementSibling.textContent.trim()

        el = el.nextElementSibling.nextElementSibling
    }

    // el sekarang adalah CONTAINER div
    if (el && el.tagName === 'DIV') {
        const placements = Array.from(el.querySelectorAll('h6'))
        const prizes = Array.from(el.querySelectorAll('p'))

        placements.forEach((h6, idx) => {
            const prize = prizes[idx]
            if (prize) {
                placements_prizes.items.push({
                    position: h6.textContent.trim(),
                    prize: prize.textContent.trim()
                })
            }
        })
    }
}

result.placements_prizes = placements_prizes

// ===== POINTS ALLOCATION =====
let points_allocation = {
    description: null,
    days: []
}

const paTitle = Array.from(document.querySelectorAll('h5'))
    .find(h => h.textContent.trim() === 'Points Allocation')

if (paTitle) {
    let el = paTitle.nextElementSibling

    while (el && el.tagName !== 'HR') {
        el = el.nextElementSibling
    }

    const descDiv = el?.nextElementSibling
    if (descDiv?.tagName === 'DIV') {
        points_allocation.description = descDiv.textContent.trim()
    }

    let dayDiv = descDiv?.nextElementSibling

    while (dayDiv && dayDiv.tagName === 'DIV') {
        const h6 = dayDiv.querySelector('h6')
        const contentDiv = h6?.nextElementSibling

        if (h6 && contentDiv?.tagName === 'DIV') {
            const day = {
                title: h6.textContent.trim(),
                points: []
            }

            const tables = contentDiv.querySelectorAll('table')

            tables.forEach(table => {
                const rows = table.querySelectorAll('tbody tr')

                rows.forEach(tr => {
                    const tds = tr.querySelectorAll('td')
                    if (tds.length < 2) return

                    const placement = tds[0].textContent.trim()
                    const points = tds[1].textContent.trim()

                    // SKIP header row
                    if (
                        placement.toLowerCase().includes('placement') ||
                        points.toLowerCase().includes('points')
                    ) return

                    day.points.push({
                        placement,
                        points: Number(points)
                    })
                })
            })

            // OPTIONAL: sort berdasarkan angka placement
            day.points.sort((a, b) => {
                const pa = parseInt(a.placement)
                const pb = parseInt(b.placement)
                return pa - pb
            })

            points_allocation.days.push(day)
        }

        dayDiv = dayDiv.nextElementSibling
    }
}

result.points_allocation = points_allocation

                    return result
                }
                """)

                browser.close()

            # Post-processing
            data["tournament_id"] = tournament_id
            data["url"] = url
            data["timezone"] = str(LOCAL_TZ)

            # Save raw JSON
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(f"[Tournament] Success: {tournament_id}, saved to {file_path}")
            return data

        except PlaywrightTimeoutError as e:
            logger.warning(f"[Tournament] Timeout {tournament_id} attempt {attempt}: {e}")
        except Exception as e:
            logger.error(f"[Tournament] Error {tournament_id} attempt {attempt}: {e}")

        time.sleep(3)

    logger.error(f"[Tournament] Failed fetch {tournament_id} after {retries} attempts")
    return None


def fetch_tournament_participants(tournament_id, retries=3):
    """
    Fetch tournament participants
    Saves to the same JSON file as detail if exists
    """
    url = f"{BASE_URL}/en-US/tournament/{tournament_id}/participants"
    file_path = RAW_DATA_DIR / f"{tournament_id}.json"

    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[Tournament] Fetch participants {tournament_id} attempt {attempt}")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)

                participants = page.evaluate("""
() => {
    const result = [];
    const h5s = Array.from(document.querySelectorAll('h5'));
    const title = h5s.find(h => h.textContent.trim().toLowerCase() === 'participating players');
    if (!title) return result;

    let el = title.nextElementSibling;
    while (el && el.tagName !== 'HR') el = el.nextElementSibling;
    if (!el) return result;

    const container = el.nextElementSibling;
    if (!container || container.tagName !== 'DIV') return result;

    Array.from(container.children).forEach(div => {
        const name = div.textContent.trim();
        if (name) result.push(name);
    });

    return result;
}
""")

                browser.close()

            # Save participants into existing JSON if exists
            if file_path.exists():
                with file_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}

            data["participants"] = participants

            with file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(f"[Tournament] Participants saved for {tournament_id}")
            return {"tournament_id": tournament_id, "participants": participants}

        except Exception as e:
            logger.error(f"[Tournament] Error participants {tournament_id} attempt {attempt}: {e}")
            time.sleep(3)

    logger.error(f"[Tournament] Failed fetch participants {tournament_id}")
    return None
