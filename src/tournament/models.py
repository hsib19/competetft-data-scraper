from typing import Optional, List
from pydantic import BaseModel

class Tournament(BaseModel):
    tournament_id: str
    name: str
    date: Optional[str] = None
    href: Optional[str] = None
    time: Optional[str] = None
    status: Optional[str] = None
    region: Optional[str] = None
    datetime: Optional[str] = None
    upcoming: Optional[bool] = None


class Participants(BaseModel):
    tournament_id: str
    url: str
    participants: List[str]
