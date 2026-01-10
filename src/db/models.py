import uuid
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

# ----------------------
# Regions
# ----------------------
class Region(Base):
    __tablename__ = "regions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)   # contoh: "EMEA"
    name = Column(String, nullable=False)                # contoh: "Europe, Middle East, Africa"

    # Relationships
    players = relationship("Player", back_populates="region")
    games = relationship("Game", back_populates="region")
    tournaments = relationship("TournamentSchedule", back_populates="region")


# ----------------------
# Events
# ----------------------
class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tournament_id = Column(String, unique=True, index=True, nullable=False)

    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)

    # Relationship to games
    games = relationship("Game", back_populates="event")


# ----------------------
# Schedule
# ----------------------
class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False)

    tournaments = relationship("TournamentSchedule", back_populates="schedule")


class TournamentSchedule(Base):
    __tablename__ = "tournament_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False)

    tournament_id = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    time = Column(String, nullable=False)
    name = Column(String, nullable=False)

    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=False)

    schedule = relationship("Schedule", back_populates="tournaments")
    region = relationship("Region", back_populates="tournaments")


# ----------------------
# Pro Points
# ----------------------
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


class ProPointsMeta(Base):
    __tablename__ = "pro_points_meta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    about = Column(String, nullable=True)
    seeding_description = Column(String, nullable=True)


# ----------------------
# Players
# ----------------------
class Player(Base):
    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=True)

    region = relationship("Region", back_populates="players")
    scores = relationship("Score", back_populates="player")
    lobby_entries = relationship("LobbyPlayer", back_populates="player")


# ----------------------
# Games
# ----------------------
class Game(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)

    day = Column(Integer, nullable=False)
    game_number = Column(Integer, nullable=False)

    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=False)

    event = relationship("Event", back_populates="games")
    region = relationship("Region", back_populates="games")
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
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=False)

    total_points = Column(Integer, nullable=False)
    qualified = Column(String, nullable=True)
    tiebreaker = Column(String, nullable=True)

    player = relationship("Player")
    region = relationship("Region")
