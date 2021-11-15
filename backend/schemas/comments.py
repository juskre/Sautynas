from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime

class CommentBase(BaseModel):
    text : Optional[str] = None
    date_posted : Optional[date] = datetime.now().date()
    
class CommentCreate(CommentBase):
    text : str
    
class ShowComment(CommentBase):
    text : str
    date_posted : date
    
    class Config():
        orm_mode = True