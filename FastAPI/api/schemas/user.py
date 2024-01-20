from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    user_name: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "anonymous",
                }
            ]
        }
    }


class User(UserBase):
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserCreateResponse(UserCreate):
    user_id: int
    model_config = ConfigDict(from_attributes=True)
