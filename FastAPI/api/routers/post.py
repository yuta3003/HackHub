from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.post as post_crud
import api.schemas.post as post_schema
from api.db import get_db

router = APIRouter()


@router.get("/users/{user_id}/posts", response_model=List[post_schema.Post])
async def list_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    return await post_crud.read_post(user_id=user_id, db=db)


@router.post("/users/{user_id}/posts", response_model=post_schema.PostCreateResponse)
async def create_posts(
    user_id: int, post_body: post_schema.PostCreate, db: AsyncSession = Depends(get_db)
):
    user = await post_crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await post_crud.create_post(user_id=user_id, db=db, post_create=post_body)


@router.put(
    "/users/{user_id}/posts/{post_id}", response_model=post_schema.PostCreateResponse
)
async def update_posts(
    user_id: int,
    post_id: int,
    post_body: post_schema.PostCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await post_crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    post = await post_crud.get_post(db=db, user_id=user_id, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return await post_crud.update_post(db=db, post_create=post_body, original=post)


@router.delete("/users/{user_id}/posts/{post_id}", response_model=None)
async def delete_posts(user_id: int, post_id: int, db: AsyncSession = Depends(get_db)):
    user = await post_crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    post = await post_crud.get_post(db=db, user_id=user_id, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return await post_crud.delete_post(db=db, original=post)
