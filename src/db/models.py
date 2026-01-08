import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tournament_id = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
