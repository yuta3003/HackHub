"""
Database Models Module.

This module defines SQLAlchemy database models for user and post entities.

Classes:
    - User: Represents the 'users' table in the database.
    - Post: Represents the 'posts' table in the database.

Attributes:
    - user_id (Column): Integer column representing the user ID (primary key).
    - user_name (Column): String column representing the user name.
    - password_hash (Column): String column representing the hashed password.
    - post (relationship): One-to-many relationship between User and Post models.

    - post_id (Column): Integer column representing the post ID (primary key).
    - user_id (Column): Integer column representing the foreign key to the 'users' table.
    - contents (Column): String column representing the contents of the post.
    - user (relationship): Many-to-one relationship between Post and User models.

Usage:
    - Import the 'User' and 'Post' classes.
    - Use these classes to interact with the database tables.

Example:
    from api.models.model import User, Post
    from api.db import Base

    # Your SQLAlchemy models are defined and can be used in database operations.
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    """
    Represents the 'users' table in the database.

    Attributes:
        user_id (Column): Integer column representing the user ID (primary key).
        user_name (Column): String column representing the user name.
        password_hash (Column): String column representing the hashed password.
        post (relationship): One-to-many relationship between User and Post models.
    """

    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)

    post = relationship("Post", back_populates="user", cascade="delete")


class Post(Base):
    """
    Represents the 'posts' table in the database.

    Attributes:
        post_id (Column): Integer column representing the post ID (primary key).
        user_id (Column): Integer column representing the foreign key to the 'users' table.
        contents (Column): String column representing the contents of the post.
        user (relationship): Many-to-one relationship between Post and User models.
    """

    __tablename__ = "posts"

    post_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    contents = Column(String(256))

    user = relationship("User", back_populates="post")
