from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime

class PostBase(BaseModel):
    title : Optional[str] = None
    text : Optional[str] = None
    additional_url : Optional[str] = None
    date_posted : Optional[date] = datetime.now().date()
    
class PostCreate(PostBase):
    title :str
    text : str
    additional_url : str
    
class ShowPost(PostBase):
    title : str
    text : str
    additional_url : Optional[str]
    date_posted : date
    
    class Config():
        orm_mode = True