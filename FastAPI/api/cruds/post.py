from sqlalchemy.ext.asyncio import AsyncSession

import api.models.model as model
import api.schemas.post as post_schema


async def create_post(
    db: AsyncSession, post_create: post_schema.PostCreate
) -> model.Post:
    post = model.Post(**post_create.dict())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post
