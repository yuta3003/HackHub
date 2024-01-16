from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class Post(BaseModel):
    id: int
    contents: Optional[str] = Field(None)

class PostCreate(BaseModel):
    id: int
