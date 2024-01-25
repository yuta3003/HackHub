from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.model as model
import api.schemas.token as token_schema
from api.db import get_db
import api.schemas.user as user_schema

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

# ユーザー情報を用いてユーザーDBから該当ユーザーを検索する
# def get_user(db, username:str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)

# async def get_user_by_name(db: AsyncSession, user_name: str) -> Optional[model.User]:
#     result: Result = await db.execute(
#         select(model.User).filter(model.User.user_name == user_name)
#     )
#     user: Optional[Tuple[model.User]] = result.first()
#     return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


# リクエストヘッダからユーザ名を返却
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

    return token_data.username

    # user = get_user_by_name(db=Depends(get_db), user_name=token_data.username)

    # if user is None:
    #     raise credentials_exception
    # return user


# async def get_current_active_user(
#     current_user: Annotated[model.User, Depends(get_current_user)]
# ):
#     # if current_user.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     # print(current_user)
#     return current_user

# # ユーザー情報が有効かどうかを調べ、有効だったらユーザー情報を返す
# async def get_current_active_user(
#     current_user: Annotated[user_schema.User, Depends(get_current_user)]
# ):
#     # if current_user.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# async def get_user_by_name(db: AsyncSession, user_name: str) -> Optional[model.User]:
#     result: Result = await db.execute(
#         select(model.User).filter(model.User.user_name == user_name)
#     )
#     user: Optional[Tuple[model.User]] = result.first()
#     return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


# ユーザー認証関数
# def get_current_user(token: str = Depends(oauth2_scheme)) -> token_schema.User:
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = get_user_by_name(db, username)
#     if user is None:
#         raise credentials_exception
#     return user

# def verify_token(token: str):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         sub = payload.get("sub")
#         if sub is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     # ここでトークンの有効期限などを追加の検証できます

#     return sub


# # リクエストヘッダに含まれるJWTからユーザー情報を取得し、該当するユーザーの情報を返す
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = token_schema.TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     # user = get_user(fake_users_db, username=token_data.username)
#     db: AsyncSession = get_db()
#     user = get_user_by_name(db=db, user_name=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# # ユーザー情報が有効かどうかを調べ、有効だったらユーザー情報を返す
# async def get_current_active_user(
#     current_user: Annotated[model.User, Depends(get_current_user)]
# ):
#     # if current_user.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
