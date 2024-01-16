from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.user as user_crud
import api.schemas.user as user_schema
from api.db import get_db

router = APIRouter()

@router.get("/users", response_model=List[user_schema.User])
async def list_users():
    pass

@router.post("/users")
async def create_users():
    pass

@router.put("/users/{user_id}")
async def update_users():
    pass

@router.put("/users/{user_id}")
async def update_users():
    pass
