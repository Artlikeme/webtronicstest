from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=True)

    posts = relationship("Post", back_populates="owner")
    likes = relationship("PostLike", back_populates="owner")

