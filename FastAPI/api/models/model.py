from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(1024), nullable=False)

    post = relationship("Post", back_populates="user", cascade="delete")

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    contents = Column(String(256))

    user = relationship("User", back_populates="post")
