from pydantic import BaseModel

class Event(BaseModel):
    tournament_id: str                
    name: str                    
    category: str = None   
    type: str = None      
    url: str = None       
