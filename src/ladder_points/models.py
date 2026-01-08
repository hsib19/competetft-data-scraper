from pydantic import BaseModel

class LadderPoint(BaseModel):
    player_id: str
    points: int
    rank: int
