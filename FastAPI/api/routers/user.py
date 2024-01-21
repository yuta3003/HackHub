from typing import List

import pymysql
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.user as user_crud
import api.schemas.user as user_schema
from api.db import get_db
from api.utils.hash_generator import HashGenerator

router = APIRouter()


@router.get("/users", response_model=List[user_schema.User])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.read_user(db=db)


@router.post("/users", response_model=user_schema.UserCreateResponse)
async def create_users(
    user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    try:
        password_hash = HashGenerator().hash_string(user_body.password_hash)
        user_body.password_hash = password_hash
        created_user = await user_crud.create_user(db=db, user_create=user_body)
        return created_user
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="User Name is already exists")


@router.put("/users/{user_id}", response_model=user_schema.UserCreateResponse)
async def update_users(
    user_id: int, user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.update_user(db=db, user_create=user_body, original=user)


@router.delete("/users/{user_id}", response_model=None)
async def delete_users(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.delete_user(db=db, original=user)
