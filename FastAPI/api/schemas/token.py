from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
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
    access_token: Optional[str] = Field(None)
    token_type: Optional[str] = Field(None)


class TokenData(BaseModel):
    username: Optional[str] = Field(None)


class User(BaseModel):
    username: str
