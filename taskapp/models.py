from datetime import datetime

from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.db import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    posts = relationship("Post", back_populates="owner")




class Post(Base):  # Изменили с Posts на Post
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="posts")
