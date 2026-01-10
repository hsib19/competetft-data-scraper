# TFT Data Scraper (Experimental)

⚠️ **Status: Experimental**

This project is **experimental** because, as of now, **Riot Games does not provide an official API** that fully supports the required **competitive and tournament-level TFT data**. All approaches used here are considered **temporary workarounds** until an official solution becomes available.

---

## Overview

TFT Data Scraper is an experimental backend project designed to **collect, normalize, and analyze Teamfight Tactics (TFT) data** from various **publicly available web sources**.

The main purpose of this project is to:

* Overcome limitations of the current Riot API
* Support analysis of TFT tournaments and competitive scenes
* Serve as a foundation for future projects such as **TFT Insight / Highlight Analyzer**

🚧 **Not intended for production use.** The implementation may change frequently.

---

## Project Goals

* Scrape TFT tournament data (matches, placements, points)
* Link VODs or clips with game metadata
* Produce structured outputs for further analysis
* Validate feasibility before an official Riot API is available

---

## Why Scraping?

The current Riot API has several limitations for competitive TFT use cases:

* No official endpoints for **detailed TFT tournament data**
* Limited access to competitive metrics (e.g., ladder points, pro points)
* Missing direct relationships between matches, players, and VODs

As a result, scraping publicly available data becomes the only viable approach for experimentation and research.

---

## Tech Stack (Experimental)

* **Python**
* **Playwright / Requests** for web scraping
* **BeautifulSoup / DOM evaluation** for data extraction
* **PostgreSQL or JSON output** (depending on use case)
* **FFmpeg + OCR (optional)** for VOD / clip analysis

---

## Output

Depending on the module, the scraper may generate:

* Normalized JSON files
* Tournament & match metadata
* Player participation and placement data
* References to VOD timestamps or clips

---

## Future Plans

* Replace scraping logic with official Riot API when available
* Improve data accuracy & validation
* Integrate directly with **TFT Insight frontend**
* Automate highlight and insight generation

---

## Disclaimer

This project is **not affiliated with Riot Games**.

Teamfight Tactics and Riot Games are trademarks or registered trademarks of Riot Games, Inc.
