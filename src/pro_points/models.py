import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.db.models import Base  

class ProPointsPlayer(Base):
    __tablename__ = "pro_points_players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rank = Column(Integer, nullable=False)
    nickname = Column(String, nullable=False)
    main_char = Column(String, nullable=False)
    total_points = Column(Integer, default=0)
    demacia_cup_total = Column(Integer, default=0)
    bilgewater_cup_total = Column(Integer, default=0)
    shurima_cup_total = Column(Integer, default=0)
    tournament_id = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)


class ProPointsSeeding(Base):
    __tablename__ = "pro_points_seeding"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
