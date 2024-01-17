from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

#import api.cruds.post as post_crud
import api.schemas.post as post_schema
#from api.db import get_db

router = APIRouter()

@router.get("/users/{user_id}/posts", response_model=List[post_schema.Post])
async def list_posts(user_id: int):
    return [post_schema.Post(user_id=user_id, post_id=1, contents="Test!!")]

@router.post("/users/{user_id}/posts", response_model=post_schema.PostCreateResponse)
async def create_posts(user_id: int, post_body: post_schema.PostCreate):
    return post_schema.PostCreateResponse(post_id=1, **post_body.dict())

@router.put("/posts/{post_id}", response_model=post_schema.PostCreateResponse)
async def update_posts(post_id: int, contents: post_schema.PostCreate):
    return post_schema.PostCreateResponse(user_id=user_id, **post_body.dict())

@router.delete("/posts/{post_id}", response_model=None)
async def delete_posts(post_id: int):
    return
