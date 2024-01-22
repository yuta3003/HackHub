from typing import List

import pymysql
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.token as token_crud
import api.schemas.token as token_schema
from api.db import get_db

router = APIRouter()

# ダミーのユーザーデータベース（実際のアプリケーションではデータベースを使用してください）
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": "fakehashedpassword",
    }
}

# ログインエンドポイント
@router.post("/token", response_model=token_schema.TokenResponse)
# def login_for_access_token(auth_info: token_schema.Token):
def login_for_access_token(auth_info: dict):
    user = fake_users_db.get(auth_info["username"])
    if user and auth_info["password"] == "fakepassword":  # 実際のアプリケーションではパスワードをハッシュ化して比較するなどセキュアな方法を使用してください
        token_data = {"sub": auth_info["username"]}
        return {"access_token": token_crud.create_token(token_data), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

# プロファイル取得エンドポイント
@router.get("/users/me", response_model=token_schema.User)
def read_users_me(current_user: dict = Depends(token_crud.get_current_user)):
    return current_user
