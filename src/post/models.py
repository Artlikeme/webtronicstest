from sqlalchemy import Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="posts")
    likes = relationship("PostLike", back_populates="posts")


class PostLike(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    like = Column(Boolean, nullable=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="likes")
    posts = relationship("Post", back_populates="likes")
