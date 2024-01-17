from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

#import api.cruds.user as user_crud
import api.schemas.user as user_schema
#from api.db import get_db

router = APIRouter()

@router.get("/users", response_model=List[user_schema.User])
async def list_users():
    return [user_schema.User(user_id=1, user_name="anonymous")]

@router.post("/users", response_model=user_schema.UserCreateResponse)
async def create_users(user_body: user_schema.UserCreate):
    return user_schema.UserCreateResponse(user_id=1, **user_body.dict())

@router.put("/users/{user_id}", response_model=user_schema.UserCreateResponse)
async def update_users(user_id: int, user_body: user_schema.UserCreate):
    return user_schema.UserCreateResponse(user_id=user_id, **user_body.dict())

@router.delete("/users/{user_id}", response_model=None)
async def delete_users(user_id: int):
    return
