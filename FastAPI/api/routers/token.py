from typing import Annotated, List

import pymysql
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.token as token_crud
import api.schemas.token as token_schema
from api.db import get_db
# from api.schemas.oauth2 import oauth2_scheme
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
        access_token = token_crud.create_token({"sub": auth_info.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    raise HTTPException(status_code=401, detail="Incorrect username or password")


# @router.get("/protected_resource", tags=["protected"], response_model=dict)
# async def get_protected_resource(token: str = Depends(oauth2_scheme)):
#     sub = token_crud.verify_token(token)
#     return {"message": f"You have access to this protected resource! (User: {sub})"}

# @router.get("/protected_resource", tags=["protected"], response_model=dict)
# async def get_protected_resource(
#     current_user: str = Depends(token_crud.get_current_user),
# ):
#     # sub = token_crud.verify_token(token)
#     return {"token": token}
#     # return {"message": f"You have access to this protected resource! (User: {sub})"}

# エンドポイントの例
# @router.get("/protected_resource1", tags=["protected"], response_model=dict)
# async def get_protected_resource(
#     token: str = Depends(token_crud.get_current_user),
# ):
#     # tokenを使った認証や処理を行う
#     # 例として、tokenをそのまま返す
#     return {"token": token}
