from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.model as model
import api.schemas.token as token_schema
import api.schemas.user as user_schema
from api.db import get_db
from api.schemas.oauth2 import oauth2_scheme

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_username_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    return token_data.username

# リクエストヘッダに含まれるJWTからユーザー情報を取得し、該当するユーザーの情報を返す
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    db = get_db()
    user = await get_user_by_name(db=db, user_name=token_data.username)

    print("--------------------------------------------------")
    print("")
    print("")
    print(user)
    print("")
    print("")
    print("--------------------------------------------------")
    if user is None:
        raise credentials_exception
    return user


async def get_user_by_name(db: AsyncSession, user_name: str) -> Optional[model.User]:
    result: Result = await db.execute(
        select(model.User).filter(model.User.user_name == user_name)
    )
    user: Optional[Tuple[model.User]] = result.first()
    return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す
# async def get_user_by_name(db: AsyncSession, user_name: str) -> Optional[model.User]:
#     async with db.begin():
#         result = await db.execute(
#             select(model.User).filter(model.User.user_name == user_name)
#         )
#         user: Optional[model.User] = result.scalar_one_or_none()
#         return user
