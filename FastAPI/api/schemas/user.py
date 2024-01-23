from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    user_name: Optional[str] = Field(None)


class User(UserBase):
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
