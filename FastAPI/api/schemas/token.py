"""
Token Models Module.

This module defines Pydantic models for representing token and user-related data structures.

Classes:
    - Token: Model representing a token with optional username and password.
    - TokenResponse: Model representing the response for a token request.
    - TokenData: Model representing data extracted from a token.
    - User: Model representing user data with optional username and password.

Usage:
    - Import the required model classes.
    - Use these models for validating and handling token and user-related data.

Example:
    from token_models import Token, TokenResponse

    token_data = {"username": "john_doe", "password": "P@ssw0rd"}
    token = Token(**token_data)

    token_response_data = {"access_token": "abcdef123456", "token_type": "bearer"}
    token_response = TokenResponse(**token_response_data)
"""
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    """
    Model representing a token with optional username and password.
    """

    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "anonymous",
                    "password": "fakepassword",
                }
            ]
        }
    }


class TokenResponse(BaseModel):
    """
    Model representing the response for a token request.
    """

    access_token: Optional[str] = Field(None)
    token_type: Optional[str] = Field(None)


class TokenData(BaseModel):
    """
    Model representing data extracted from a token.
    """

    username: Union[str, None] = None
