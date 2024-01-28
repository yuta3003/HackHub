"""
Post API Router.

This module defines FastAPI routes for managing post-related operations.

Classes:
    - router: FastAPI APIRouter instance for post operations.

Routes:
    - GET /users/{user_id}/posts: List posts for a specific user.
    - POST /user/{user_id}/posts: Create a new post for a specific user.
    - PUT /users/{user_id}/posts/{post_id}: Update an existing post for a specific user.
    - DELETE /users/{user_id}/posts/{post_id}: Delete an existing post for a specific user.

Usage:
    - Import the 'router' instance.
    - Include the router in your FastAPI app.

Example:
    from fastapi import FastAPI
    from api.routers import post

    app = FastAPI()
    app.include_router(post.router)

    # Your FastAPI app now includes the post routes.
"""
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.post as post_crud
import api.cruds.token as token_crud
import api.schemas.post as post_schema
import api.schemas.user as user_schema
from api.db import get_db

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.get("/users/{user_id}/posts", response_model=List[post_schema.Post])
async def list_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    List posts for a specific user.

    Args:
        user_id (int): ID of the user for whom to list posts.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        List[post_schema.Post]: List of post data for the specified user.

    Raises:
        HTTPException: If the specified user is not found.
    """
    return await post_crud.read_post(user_id=user_id, db=db)


@router.post(
    "/users/{user_id}/posts",
    dependencies=[Depends(bearer_scheme)],
    response_model=post_schema.PostCreateResponse,
)
async def create_posts(
    auth_user: Annotated[user_schema.User, Depends(token_crud.get_current_user)],
    post_body: post_schema.PostCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new post for a specific user.

    Args:
        auth_user (Annotated[user_schema.User]): Authenticated user data.
        post_body (post_schema.PostCreate): Request body containing post data.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        post_schema.PostCreateResponse: Created post data.

    Raises:
        HTTPException: If the specified user is not found.
    """
    return await post_crud.create_post(
        user_id=auth_user.user_id, db=db, post_create=post_body
    )


@router.put(
    "/users/{user_id}/posts/{post_id}",
    dependencies=[Depends(bearer_scheme)],
    response_model=post_schema.PostCreateResponse,
)
async def update_posts(
    auth_user: Annotated[user_schema.User, Depends(token_crud.get_current_user)],
    post_id: int,
    post_body: post_schema.PostCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing post for a specific user.

    Args:
        auth_user (Annotated[user_schema.User]): Authenticated user data.
        post_id (int): ID of the post to update.
        post_body (post_schema.PostCreate): Request body containing updated post data.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        post_schema.PostCreateResponse: Updated post data.

    Raises:
        HTTPException: If the specified user or post is not found.
    """
    post = await post_crud.get_post(db=db, user_id=auth_user.user_id, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return await post_crud.update_post(db=db, post_create=post_body, original=post)


@router.delete(
    "/users/{user_id}/posts/{post_id}",
    dependencies=[Depends(bearer_scheme)],
    response_model=None,
)
async def delete_posts(
    auth_user: Annotated[user_schema.User, Depends(token_crud.get_current_user)],
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an existing post for a specific user.

    Args:
        auth_user (Annotated[user_schema.User]): Authenticated user data.
        post_id (int): ID of the post to delete.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        None

    Raises:
        HTTPException: If the specified user or post is not found.
    """

    post = await post_crud.get_post(db=db, user_id=auth_user.user_id, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return await post_crud.delete_post(db=db, original=post)
