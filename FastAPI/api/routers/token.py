from typing import Annotated, List

import pymysql
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.token as token_crud
import api.cruds.user as user_crud
import api.schemas.token as token_schema
import api.schemas.user as user_schema
from api.db import get_db
from api.utils.hash_generator import HashGenerator


# from api.schemas.oauth2 import oauth2_scheme

router = APIRouter()
bearer_scheme = HTTPBearer()

# # JWTの設定を定義
# class Settings(BaseModel):
#     authjwt_secret_key: str = "your-secret-key"
#     authjwt_token_location: set = {"headers"}
#     authjwt_algorithm: str = "HS256"

# @AuthJWT.load_config
# def get_config():
#     return Settings()

# ログインエンドポイント
@router.post("/token", response_model=token_schema.TokenResponse)
async def login_for_access_token(
    auth_info: token_schema.Token, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_by_name(db=db, user_name=auth_info.username)
    password_hash = HashGenerator().hash_string(auth_info.password)
    if user.password_hash == password_hash:
        access_token = token_crud.create_access_token(
            data={"sub": auth_info.username}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.get("/protected", dependencies=[Depends(bearer_scheme)])
async def protected_endpoint(
    user_name: Annotated[str, Depends(token_crud.get_current_user)]
    # current_user: Annotated[user_schema.User, Depends(token_crud.get_current_active_user)]
):
    # この部分にはトークンが検証されている状態での処理を書く
    return {"message": "ok"}
# def protected(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#     current_user = Authorize.get_jwt_subject()
#     return {"user": current_user}


# @router.get("/protected_resource", tags=["protected"], response_model=dict)
# async def get_protected_resource(token: str = Depends(oauth2_scheme)):
#     sub = token_crud.verify_token(token)
#     return {"message": f"You have access to this protected resource! (User: {sub})"}

# @router.get("/users/me/items")
# async def read_own_items(
#     current_user: Annotated[user_schema.User, Depends(token_crud.get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]

# @router.get("/protected_resource", tags=["protected"], response_model=dict, dependencies=[Depends(bearer_scheme)])
# async def get_protected_resource(
#     current_user: str = Depends(token_crud.get_current_user),
# ):
#     # sub = token_crud.verify_token(token)
#     return {"current_user": current_user}
#     # return {"message": f"You have access to this protected resource! (User: {sub})"}

# エンドポイントの例
# @router.get("/protected_resource1", tags=["protected"], response_model=dict)
# async def get_protected_resource(
#     token: str = Depends(token_crud.get_current_user),
# ):
#     # tokenを使った認証や処理を行う
#     # 例として、tokenをそのまま返す
#     return {"token": token}
