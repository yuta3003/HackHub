"""
Authentication and Token Endpoints Module.

This module defines FastAPI routes for handling user authentication and token-related operations.

Classes:
    - router: FastAPI APIRouter instance for authentication and token operations.

Routes:
    - POST /token: Obtain an access token by providing username and password.
    - GET /get-current-user: Get information about the currently authenticated user.

Usage:
    - Import the 'router' instance.
    - Include the router in your FastAPI app.

Example:
    from fastapi import FastAPI
    from api.routers import auth

    app = FastAPI()
    app.include_router(auth.router)

    # Your FastAPI app now includes the authentication and token routes.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
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
    """
    Obtain an access token by providing username and password.

    Args:
        auth_info (token_schema.Token): Token schema containing username and password.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        token_schema.TokenResponse: Response containing the access token and token type.

    Raises:
        HTTPException: If the provided username or password is incorrect.
    """
    user = await user_crud.get_user_by_name(db=db, user_name=auth_info.user_name)
    password_hash = HashGenerator().hash_string(auth_info.password)
    if user.password_hash == password_hash:
        access_token = token_crud.create_access_token(data={"sub": auth_info.user_name})
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    raise HTTPException(status_code=401, detail="Incorrect user_name or password")


@router.get("/get-current-user", dependencies=[Depends(bearer_scheme)])
async def get_current_usermodel(
    auth_user: Annotated[user_schema.User, Depends(token_crud.get_current_user)]
):
    """
    Get information about the currently authenticated user.

    Args:
        auth_user (Annotated[user_schema.User]): Authenticated user data.

    Returns:
        dict: Response message containing the username of the authenticated user.
    """
    return {"message": auth_user.user_name}
