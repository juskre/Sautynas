from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(String,nullable=False)
    additional_url = Column(String)
    date_posted = Column(Date)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User",back_populates="posts")