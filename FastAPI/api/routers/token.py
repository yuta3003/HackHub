from typing import List

import pymysql
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.token as token_crud
import api.schemas.token as token_schema
from api.db import get_db
from api.utils.hash_generator import HashGenerator

router = APIRouter()

# ログインエンドポイント
@router.post("/token", response_model=token_schema.TokenResponse)
async def login_for_access_token(
    auth_info: token_schema.Token, db: AsyncSession = Depends(get_db)
):
    user = await token_crud.get_user_by_name(db=db, user_name=auth_info.username)
    password_hash = HashGenerator().hash_string(auth_info.password)
    if user.password_hash == password_hash:
        token_data = {"sub": auth_info.username}
        return {
            "access_token": token_crud.create_token(token_data),
            "token_type": "bearer",
        }
    raise HTTPException(status_code=401, detail="Incorrect username or password")


# プロファイル取得エンドポイント
@router.get("/users/me", response_model=token_schema.User)
def read_users_me(current_user: dict = Depends(token_crud.get_current_user)):
    return current_user
