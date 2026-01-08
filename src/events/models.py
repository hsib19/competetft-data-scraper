from pydantic import BaseModel

class Event(BaseModel):
    id: str
    name: str
    start_date: str
    end_date: str
