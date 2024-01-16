from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
    id: int

class UserCreate(BaseModel):
    id: int
