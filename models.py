from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key= True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, index=True, default=False)