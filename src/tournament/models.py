from pydantic import BaseModel
from datetime import datetime

class Tournament(BaseModel):
    tournament_id: str
    href: str
    time: str           
    name: str
    region: str
    datetime: datetime  
    upcoming: bool


class Participant(BaseModel):
    id: str
    name: str
    rank: int
