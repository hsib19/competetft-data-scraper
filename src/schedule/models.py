from pydantic import BaseModel

class ScheduleItem(BaseModel):
    event_id: str
    date: str
    match_url: str
