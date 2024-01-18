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

async def read_post(db: AsyncSession) -> List[Tuple[int, int, str]]:
    result: Result = await (
        db.execute(
            select(
                model.Post.post_id,
                model.Post.user_id,
                model.Post.contents,
            )
        )
    )
    return result.all()
