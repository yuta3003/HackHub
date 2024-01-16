from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

#import api.cruds.post as post_crud
import api.schemas.post as post_schema
#from api.db import get_db

router = APIRouter()

@router.get("/users/{user_id}/post", response_model=post_schema.Post)
async def list_posts():
    return [post_schema.Post(id=1, contents="Test Contents")]

@router.post("/users/{user_id}/post", response_model=post_schema.PostCreateResponse)
async def create_posts(post_bod):
    pass

@router.put("/users/{user_id}/post/{post_id}", response_model=post_schema.PostCreateResponse)
async def update_posts():
    pass

@router.delete("/users/{user_id}/post/{post_id}", response_model=None)
async def delete_posts():
    pass


@router.post("/users", response_model=user_schema.UserCreateResponse)
async def create_users(user_body: user_schema.UserCreate):
    return user_schema.UserCreateResponse(id=1, **user_body.dict())

@router.put("/users/{user_id}", response_model=user_schema.UserCreateResponse)
async def update_users(user_id: int, user_body: user_schema.UserCreate):
    return user_schema.UserCreateResponse(id=user_id, **user_body.dict())

@router.delete("/users/{user_id}", response_model=None)
async def delete_users(user_id: int):
    return
