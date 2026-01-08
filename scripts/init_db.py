import sys
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.db.models import Base  
from src.db.session import engine

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print("Failed to connect or create tables:", e)

if __name__ == "__main__":
    init_db()
