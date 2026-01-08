import uuid
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

# Base class for all ORM models
Base = declarative_base()

class Schedule(Base):
    __tablename__ = "schedules"

    # Primary key with UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Date of the schedule
    date = Column(Date, nullable=False)

    # Relationship to TournamentSchedule (one schedule can have many tournaments)
    tournaments = relationship("TournamentSchedule", back_populates="schedule")


class TournamentSchedule(Base):
    __tablename__ = "tournament_schedules"

    # Primary key with UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key linking to Schedule
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False)

    # Tournament-specific fields
    tournament_id = Column(String, index=True, nullable=False) 
    url = Column(String, nullable=False)                                     # Link to tournament page
    time = Column(String, nullable=False)                                    # Time as string (can convert to Time type)
    name = Column(String, nullable=False)                                    # Tournament name
    region = Column(String, nullable=False)                                  # Region of the tournament

    # Relationship back to Schedule
    schedule = relationship("Schedule", back_populates="tournaments")
