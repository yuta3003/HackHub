from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    user_id: int
    contents: Optional[str] = Field(None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "contents": "Contents",
                }
            ]
        }
    }

class Post(PostBase):
    post_id: int
    model_config = ConfigDict(from_attributes=True)

class PostCreate(PostBase):
    pass

class PostCreateResponse(PostCreate):
    post_id: int
    model_config = ConfigDict(from_attributes=True)
