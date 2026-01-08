import uuid
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Date, ForeignKey
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
