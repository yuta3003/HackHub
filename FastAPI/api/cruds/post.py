from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.model as model
import api.schemas.post as post_schema


async def create_post(
    user_id, db: AsyncSession, post_create: post_schema.PostCreate
) -> model.Post:
    post = model.Post(user_id=user_id, **post_create.dict())
    db.add(post)
    await db.flush()
    await db.commit()
    await db.refresh(post)
    return post


async def read_post(user_id: int, db: AsyncSession) -> List[Tuple[int, int, str]]:
    result: Result = await db.execute(
        select(
            model.Post.post_id,
            model.Post.user_id,
            model.Post.contents,
        ).filter(model.Post.user_id == user_id)
    )
    return result.all()


async def get_user(db: AsyncSession, user_id: int) -> Optional[model.User]:
    result: Result = await db.execute(
        select(model.User).filter(model.User.user_id == user_id)
    )
    user: Optional[Tuple[model.User]] = result.first()
    return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


async def get_post(
    db: AsyncSession, user_id: int, post_id: int
) -> Optional[model.Post]:
    result: Result = await db.execute(
        select(model.Post).filter(
            model.Post.user_id == user_id, model.Post.post_id == post_id
        )
    )
    post: Optional[Tuple[model.Post]] = result.first()
    return post[0] if post else None


async def update_post(
    db: AsyncSession, post_create: post_schema.PostCreate, original: model.Post
) -> model.Post:
    original.contents = post_create.contents
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_post(db: AsyncSession, original: model.Post) -> None:
    await db.delete(original)
    await db.commit()
