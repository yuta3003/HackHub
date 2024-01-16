from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.post as post_crud
import api.schemas.post as post_schema
from api.db import get_db

router = APIRouter()

@router.get("/users/{user_id}/post")
async def list_posts():
    pass

@router.post("/users/{user_id}/post")
async def create_posts():
    pass

@router.put("/users/{user_id}/post/{post_id}")
async def update_posts():
    pass

@router.put("/users/{user_id}/post/{post_id}")
async def delete_posts():
    pass
