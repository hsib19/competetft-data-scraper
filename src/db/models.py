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

# ----------------------
# Players
# ----------------------
class Player(Base):
    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    region = Column(String, nullable=True)

    # Relationship to scores and lobby participation
    scores = relationship("Score", back_populates="player")
    lobby_entries = relationship("LobbyPlayer", back_populates="player")


# ----------------------
# Games
# ----------------------
class Game(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tournament_id = Column(String, index=True, nullable=False)
    day = Column(Integer, nullable=False)
    game_number = Column(Integer, nullable=False)

    # Relationship to scores and lobbies
    scores = relationship("Score", back_populates="game")
    lobbies = relationship("Lobby", back_populates="game")


# ----------------------
# Scores
# ----------------------
class Score(Base):
    __tablename__ = "scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    score = Column(Integer, nullable=False)

    # Relationships
    player = relationship("Player", back_populates="scores")
    game = relationship("Game", back_populates="scores")


# ----------------------
# Lobbies
# ----------------------
class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    lobby_number = Column(Integer, nullable=False)

    # Relationship to lobby players
    game = relationship("Game", back_populates="lobbies")
    players = relationship("LobbyPlayer", back_populates="lobby")


# ----------------------
# Lobby Players
# ----------------------
class LobbyPlayer(Base):
    __tablename__ = "lobby_players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lobby_id = Column(UUID(as_uuid=True), ForeignKey("lobbies.id"), nullable=False)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    placement = Column(Integer, nullable=True)
    score = Column(Integer, nullable=False)

    # Relationships
    lobby = relationship("Lobby", back_populates="players")
    player = relationship("Player", back_populates="lobby_entries")


# ----------------------
# Daily Results
# ----------------------
class DailyResult(Base):
    __tablename__ = "daily_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    tournament_id = Column(String, index=True, nullable=False)
    day = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)
    qualified = Column(String, nullable=True)  # e.g. "Qualified", "Eliminated", "Pending"
    tiebreaker = Column(String, nullable=True)  # e.g. "8 Top 4s, 2 Wins"

    player = relationship("Player")
