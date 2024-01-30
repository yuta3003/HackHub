"""
User API Router.

This module defines FastAPI routes for managing user-related operations.

Classes:
    - router: FastAPI APIRouter instance for user operations.

Routes:
    - GET /users: List all users.
    - POST /users: Create a new user.
    - PUT /users/{user_id}: Update an existing user.
    - DELETE /users/{user_id}: Delete an existing user.

Usage:
    - Import the 'router' instance.
    - Include the router in your FastAPI app.

Example:
    from fastapi import FastAPI
    from api.routers import user

    app = FastAPI()
    app.include_router(user.router)

    # Your FastAPI app now includes the user routes.
"""
from typing import Annotated, List

import pymysql
import starlette.status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import sqlite3

import api.cruds.token as token_crud
import api.cruds.user as user_crud
import api.schemas.user as user_schema
from api.db import get_db
from api.utils import HashGenerator
from api.exceptions import IntegrityViolationError

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.get("/users", response_model=List[user_schema.User])
async def list_users(db: AsyncSession = Depends(get_db)):
    """
    Get a list of all users.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        List[user_schema.User]: List of user data.

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    return await user_crud.read_user(db=db)


@router.post("/users", response_model=user_schema.UserCreateResponse)
async def create_users(
    user_body: user_schema.UserCreateRequest, db: AsyncSession = Depends(get_db)
):
    """
    Create a new user.

    Args:
        user_body (user_schema.UserCreateRequest): Request body containing user data.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        user_schema.UserCreateResponse: Created user data.

    Raises:
        HTTPException: If an error occurs during the operation, such as duplicate user name.
    """
    try:
        password_hash = HashGenerator().hash_string(user_body.password)
        user_create = user_schema.UserCreate(
            user_name=user_body.user_name, password_hash=password_hash
        )
        created_user = await user_crud.create_user(db=db, user_create=user_create)
        return created_user
    except IntegrityViolationError:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="User Name is already exists",
        )
    # except pymysql.err.IntegrityError:
    #     raise HTTPException(
    #         status_code=starlette.status.HTTP_400_BAD_REQUEST,
    #         detail="User Name is already exists",
    #     )
    # except sqlite3.IntegrityError:
    #     raise HTTPException(
    #         status_code=starlette.status.HTTP_400_BAD_REQUEST,
    #         detail="User Name is already exists",
    #     )


@router.put(
    "/users/{user_id}",
    dependencies=[Depends(bearer_scheme)],
    response_model=user_schema.UserCreateResponse,
)
async def update_users(
    auth_user: Annotated[user_schema.User, Depends(token_crud.get_current_user)],
    user_body: user_schema.UserCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing user.

    Args:
        auth_user (Annotated[user_schema.User]): Authenticated user data.
        user_body (user_schema.UserCreateRequest): Request body containing updated user data.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        user_schema.UserCreateResponse: Updated user data.

    Raises:
        HTTPException: If an error occurs during the operation.
    """

    password_hash = HashGenerator().hash_string(user_body.password)
    user_create = user_schema.UserCreate(
        user_name=user_body.user_name, password_hash=password_hash
    )
    return await user_crud.update_user(
        db=db, user_create=user_create, original=auth_user
    )


@router.delete(
    "/users/{user_id}", dependencies=[Depends(bearer_scheme)], response_model=None
)
async def delete_users(
    auth_user: Annotated[user_schema.User, Depends(token_crud.get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an existing user.

    Args:
        auth_user (Annotated[user_schema.User]): Authenticated user data.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        None

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    return await user_crud.delete_user(db=db, original=auth_user)
