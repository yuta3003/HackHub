from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    user_name: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "anonymous",
                    "password_hash": "77cc538aa9b72abb040bb087d1358d58dec3f9b8e817de96af457807d083b5df",
                }
            ]
        }
    }


class User(UserBase):
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password_hash: Optional[str] = Field(None)


class UserCreateResponse(UserCreate):
    user_id: int
    model_config = ConfigDict(from_attributes=True)
