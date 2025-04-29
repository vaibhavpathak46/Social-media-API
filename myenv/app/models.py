from .database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, func
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.types import TIMESTAMP, TIME, DateTime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True ,nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP (timezone=True),nullable=False, server_default=func.now())
   
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True ,nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP (timezone=True),nullable=False, server_default=func.now())
    posts = relationship("Post", back_populates="owner")