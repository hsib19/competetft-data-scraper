from pydantic import BaseModel

class Tournament(BaseModel):
    id: str
    name: str
    date: str

class Participant(BaseModel):
    id: str
    name: str
    rank: int
