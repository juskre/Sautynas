from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    date_posted = Column(Date)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User",back_populates="comments")
    