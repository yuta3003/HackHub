"""
Post CRUD Operations Module.

This module provides functions for performing CRUD (Create, Read, Update, Delete) operations on the 'posts' table.

Functions:
    - create_post: Create a new post in the database.
    - read_post: Retrieve a list of posts by user ID from the database.
    - get_post: Retrieve a post by post ID and user ID from the database.
    - update_post: Update an existing post in the database.
    - delete_post: Delete an existing post from the database.

Usage:
    - Import the functions as needed.
    - Use these functions to interact with the 'posts' table in the database.

Example:
    from api.cruds.post import create_post, read_post, get_user_by_id, get_post, update_post, delete_post
    from api.schemas.post import PostCreate
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession() as session:
        # Example: Create a new post
        new_post_data = PostCreate(contents="Example post contents")
        created_post = await create_post(session, post_create=new_post_data, user_id=1)

        # Example: Read posts by user ID
        posts_list = await read_post(session, user_id=1)

        # Example: Get user by ID
        user_by_id = await get_user_by_id(session, user_id=1)

        # Example: Get post by post ID and user ID
        post_by_id = await get_post(session, post_id=created_post.post_id, user_id=1)

        # Example: Update post
        updated_post_data = PostCreate(contents="Updated post contents")
        updated_post = await update_post(session, original=created_post, post_create=updated_post_data)

        # Example: Delete post
        await delete_post(session, original=updated_post)
"""
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.post as post_schema
from api.models import model


async def create_post(
    db: AsyncSession, post_create: post_schema.PostCreate, user_id: int
) -> model.Post:
    """
    Create a new post in the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        post_create (post_schema.PostCreate): Post data for creation.
        user_id (int): ID of the user creating the post.

    Returns:
        model.Post: Created post data.
    """
    post = model.Post(user_id=user_id, **post_create.model_dump())
    db.add(post)
    await db.flush()
    await db.commit()
    await db.refresh(post)
    return post


async def read_post(db: AsyncSession, user_id: int) -> List[Tuple[int, int, str]]:
    """
    Retrieve a list of posts by user ID from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        user_id (int): ID of the user whose posts to retrieve.

    Returns:
        List[Tuple[int, int, str]]: List of tuples containing post IDs, user IDs, and post contents.
    """
    result: Result = await db.execute(
        select(
            model.Post.post_id,
            model.Post.user_id,
            model.Post.contents,
        ).filter(model.Post.user_id == user_id)
    )
    return result.all()


async def get_post(
    db: AsyncSession, post_id: int, user_id: int
) -> Optional[model.Post]:
    """
    Retrieve a post by post ID and user ID from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        post_id (int): ID of the post to retrieve.
        user_id (int): ID of the user who created the post.

    Returns:
        Optional[model.Post]: Post data if found, otherwise None.
    """
    result: Result = await db.execute(
        select(model.Post).filter(
            model.Post.user_id == user_id, model.Post.post_id == post_id
        )
    )
    post: Optional[Tuple[model.Post]] = result.first()
    return post[0] if post else None


async def update_post(
    db: AsyncSession, original: model.Post, post_create: post_schema.PostCreate
) -> model.Post:
    """
    Update an existing post in the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        original (model.Post): Original post data to be updated.
        post_create (post_schema.PostCreate): Updated post data.

    Returns:
        model.Post: Updated post data.
    """
    original.contents = post_create.contents
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_post(db: AsyncSession, original: model.Post) -> None:
    """
    Delete an existing post from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        original (model.Post): Post data to be deleted.

    Returns:
        None
    """
    await db.delete(original)
    await db.commit()
