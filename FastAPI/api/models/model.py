from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(1024), nullable=False)

    post = relationship("Post", back_populates="user", cascade="delete")

class Post(Base):
    __tablename__ = "posts"
    # __table_args__ = (
    #     PrimaryKeyConstraint('user_id', 'post_id'),
    # )

    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    contents = Column(String(256))

    user = relationship("User", back_populates="post")
