"""
User CRUD Operations Module.

This module defines asynchronous CRUD (Create, Read, Update, Delete) operations
for the 'users' table in the database.

Functions:
    - create_user: Create a new user in the database.
    - read_user: Retrieve a list of user IDs and names from the database.
    - get_user_by_id: Retrieve a user by their ID.
    - get_user_by_name: Retrieve a user by their username.
    - update_user: Update user information in the database.
    - delete_user: Delete a user from the database.

Usage:
    - Import the functions and use them to interact with the 'users' table.

Example:
    from api.cruds.user import create_user, read_user, get_user_by_id, update_user, delete_user
    from api.schemas.user import UserCreate
    from api.db import get_db

    async with get_db() as db:
        # Create a new user
        new_user = UserCreate(user_name="example_user")
        created_user = await create_user(db, user_create=new_user)

        # Read user data
        user_list = await read_user(db)

        # Get user by ID
        retrieved_user = await get_user_by_id(db, user_id=created_user.user_id)

        # Update user information
        updated_user = await update_user(db, original=retrieved_user, user_create=new_user)

        # Delete user
        await delete_user(db, original=updated_user)
"""
from typing import List, Optional, Tuple

from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.model as model
import api.schemas.user as user_schema

from api.exceptions import IntegrityViolationError


async def create_user( db: AsyncSession, user_create: user_schema.UserCreate
) -> model.User:
    """
    Create a new user in the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        user_create (user_schema.UserCreate): User creation data.

    Returns:
        model.User: Created user data.

    Raises:
        IntegrityError: If a user with the same username already exists.
    """
    try:
        user = model.User(**user_create.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise IntegrityViolationError


async def read_user(db: AsyncSession) -> List[Tuple[int, str]]:
    """
    Retrieve a list of user IDs and names from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        List[Tuple[int, str]]: List of user IDs and names.
    """
    result: Result = await db.execute(
        select(
            model.User.user_id,
            model.User.user_name,
        )
    )
    return result.all()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[model.User]:
    """
    Retrieve a user by their ID.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        user_id (int): ID of the user to retrieve.

    Returns:
        Optional[model.User]: Retrieved user data, or None if not found.
    """
    result: Result = await db.execute(
        select(model.User).filter(model.User.user_id == user_id)
    )
    user: Optional[Tuple[model.User]] = result.first()
    return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


async def get_user_by_name(db: AsyncSession, user_name: str) -> Optional[model.User]:
    """
    Retrieve a user by their username.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        user_name (str): Username of the user to retrieve.

    Returns:
        Optional[model.User]: Retrieved user data, or None if not found.
    """
    result: Result = await db.execute(
        select(model.User).filter(model.User.user_name == user_name)
    )
    user: Optional[Tuple[model.User]] = result.first()
    return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


async def update_user(
    db: AsyncSession, original: model.User, user_create: user_schema.UserCreateRequest
) -> model.User:
    """
    Update user information in the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        original (model.User): Original user data.
        user_create (user_schema.UserCreate): User creation data.

    Returns:
        model.User: Updated user data.
    """
    try:
        await db.execute(
            update(model.User)
            .where(model.User.user_id == original.user_id)
            .values(**user_create.model_dump())
        )

        await db.commit()

        await db.refresh(original)
        return original

    except IntegrityError:
        await db.rollback()
        raise IntegrityViolationError


async def delete_user(db: AsyncSession, original: model.User) -> None:
    """
    Delete an existing user from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        original (model.User): User data to be deleted.

    Returns:
        None
    """
    await db.delete(original)
    await db.commit()
