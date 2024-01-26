"""
Post Models Module.

This module defines Pydantic models for representing post-related data structures.

Classes:
    - PostBase: Base model for post data with optional contents.
    - Post: Model representing a post with user_id, post_id, and optional contents.
    - PostCreate: Model for creating a post with optional contents.
    - PostCreateResponse: Model representing the response for creating a post.

Usage:
    - Import the required model classes.
    - Use these models for validating and handling post-related data.

Example:
    from post_models import Post, PostCreate

    post_data = {"user_id": 1, "post_id": 1, "contents": "Example contents"}
    post = Post(**post_data)

    post_creation_data = {"contents": "New post contents"}
    post_creation = PostCreate(**post_creation_data)
"""
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    """
    Base model for post data with optional contents.
    """

    contents: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "contents": "Contents",
                }
            ]
        }
    }


class Post(PostBase):
    """
    Model representing a post with user_id, post_id, and optional contents.
    """

    user_id: int
    post_id: int
    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    """
    Model for creating a post with optional contents.
    """

    pass


class PostCreateResponse(PostCreate):
    """
    Model representing the response for creating a post.
    """

    user_id: int
    post_id: int
    model_config = ConfigDict(from_attributes=True)
