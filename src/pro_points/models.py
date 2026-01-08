from pydantic import BaseModel

class ProPoint(BaseModel):
    player_id: str
    points: int
    rank: int
