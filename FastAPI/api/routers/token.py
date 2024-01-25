from typing import Annotated, List

import pymysql
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.token as token_crud
import api.cruds.user as user_crud
import api.schemas.token as token_schema
import api.schemas.user as user_schema
from api.db import get_db
from api.utils.hash_generator import HashGenerator

router = APIRouter()
bearer_scheme = HTTPBearer()


# ログインエンドポイント
@router.post("/token", response_model=token_schema.TokenResponse)
async def login_for_access_token(
    auth_info: token_schema.Token, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_by_name(db=db, user_name=auth_info.username)
    password_hash = HashGenerator().hash_string(auth_info.password)
    if user.password_hash == password_hash:
        access_token = token_crud.create_access_token(data={"sub": auth_info.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.get("/protected", dependencies=[Depends(bearer_scheme)])
async def protected_endpoint(
    user_name: Annotated[str, Depends(token_crud.decode_username_from_token)]
):
    return {"message": user_name}

@router.get("/get-current-user", dependencies=[Depends(bearer_scheme)])
async def get_current_usermodel(
    user_name: Annotated[user_schema.User, Depends(token_crud.get_current_user)]
):
    return {"message": user_name.user_name}
