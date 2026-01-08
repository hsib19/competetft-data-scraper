import uuid
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

# Base class for all ORM models
Base = declarative_base()

# ----------------------
# Events
# ----------------------
class Event(Base):
    __tablename__ = "events"

    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Unique tournament identifier
    tournament_id = Column(String, unique=True, index=True, nullable=False)

    # Event metadata
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)


# ----------------------
# Schedule
# ----------------------
class Schedule(Base):
    __tablename__ = "schedules"

    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Date for the schedule
    date = Column(Date, nullable=False)

    # One-to-many relationship with TournamentSchedule
    tournaments = relationship("TournamentSchedule", back_populates="schedule")


class TournamentSchedule(Base):
    __tablename__ = "tournament_schedules"

    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key referencing schedules table
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False)

    # Tournament details
    tournament_id = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    time = Column(String, nullable=False)  # Can be changed to Time type after parsing
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)

    # Relationship back to Schedule
    schedule = relationship("Schedule", back_populates="tournaments")

# ----------------------
# Pro Points
# ----------------------
class ProPointsPlayer(Base):
    __tablename__ = "pro_points_players"

    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Player info
    rank = Column(Integer, nullable=False)
    nickname = Column(String, nullable=False)
    main_char = Column(String, nullable=False)

    # Points breakdown
    total_points = Column(Integer, default=0)
    demacia_cup_total = Column(Integer, default=0)
    bilgewater_cup_total = Column(Integer, default=0)
    shurima_cup_total = Column(Integer, default=0)

    # Tournament reference
    tournament_id = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)


class ProPointsSeeding(Base):
    __tablename__ = "pro_points_seeding"

    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Seeding rule
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class ProPointsMeta(Base):
    __tablename__ = "pro_points_meta"

    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # General description
    about = Column(String, nullable=True)
    seeding_description = Column(String, nullable=True)
