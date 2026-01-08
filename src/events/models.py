from pydantic import BaseModel, HttpUrl

class EventItem(BaseModel):
    url: str                
    tournament_id: str       
    name: str               
    type: str               
    category: str           
