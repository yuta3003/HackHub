from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.model as model
import api.schemas.user as user_schema


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> model.User:
    user = model.User(**user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def read_user(db: AsyncSession) -> List[Tuple[int, str]]:
    result: Result = await (
        db.execute(
            select(
                model.User.user_id,
                model.User.user_name,
            )
        )
    )
    return result.all()

async def get_user(db: AsyncSession, user_id: int) -> Optional[model.User]:
    result: Result = await db.execute(
        select(model.User).filter(model.User.user_id == user_id)
    )
    user: Optional[Tuple[model.User]] = result.first()
    return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す

async def update_user(
    db: AsyncSession, user_create: user_schema.UserCreate, original: model.User
) -> model.User:
    original.user_name = user_create.user_name
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_user(db: AsyncSession, original: model.User) -> None:
    await db.delete(original)
    await db.commit()
