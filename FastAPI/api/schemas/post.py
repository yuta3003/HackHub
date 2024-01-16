from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    contents: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "contents": "None",
                }
            ]
        }
    }

class Post(PostBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PostCreate(PostBase):
    pass

class PostCreateResponse(PostCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
