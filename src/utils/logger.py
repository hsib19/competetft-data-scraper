from loguru import logger
import os
from src.config.settings import LOG_DIR

os.makedirs(LOG_DIR, exist_ok=True)
logger.add(f"{LOG_DIR}/scraper.log", rotation="1 MB", retention="7 days", level="INFO")
