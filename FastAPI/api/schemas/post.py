from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class Post(BaseModel):
    id: int

class PostCreate(BaseModel):
    id: int
