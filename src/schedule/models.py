from pydantic import BaseModel
from typing import List, Optional

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

class ScheduleDay(BaseModel):
    date: str
    tournaments: List[Tournament]
