"""
User Models Module.

This module defines Pydantic models for representing user-related data structures.

Classes:
    - UserBase: Base model for user data with optional user_name.
    - User: Model representing user data with user_id and optional user_name.
    - UserCreateRequest: Model for creating a user with optional password.
    - UserCreate: Model representing a created user with password hash.
    - UserCreateResponse: Model representing the response for creating a user.

Usage:
    - Import the required model classes.
    - Use these models for validating and handling user-related data.

Example:
    from user_models import User, UserCreate

    user_data = {"user_id": 1, "user_name": "john_doe"}
    user = User(**user_data)

    user_creation_data = {"user_name": "new_user", "password": "P@ssw0rd"}
    user_creation = UserCreate(**user_creation_data)
"""
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """
    Base model for user data with optional user_name.
    """

    user_name: Optional[str] = Field(None)


class User(UserBase):
    """
    Model representing user data with user_id and optional user_name.
    """

    user_id: int
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "use_id": 1,
                    "user_name": "anonymous",
                }
            ]
        }
    }


class UserCreateRequest(UserBase):
    """
    Model for creating a user with optional password.
    """

    password: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "anonymous",
                    "password": "P@ssw0rd",
                }
            ]
        }
    }


class UserCreate(UserBase):
    """
    Model representing a created user with password hash.
    """

    password_hash: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "anonymous",
                    "password_hash": "b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342",
                }
            ]
        }
    }


class UserCreateResponse(UserCreate):
    """
    Model representing the response for creating a user.
    """

    user_id: int
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "user_name": "anonymous",
                    "password_hash": "b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342",
                }
            ]
        }
    }
