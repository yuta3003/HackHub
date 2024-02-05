"""
Authentication and Authorization Module.

This module provides functions for authentication and authorization using JWT (JSON Web Tokens).

Constants:
    - SECRET_KEY: Secret key used for JWT encoding and decoding.
    - ALGORITHM: JWT encoding algorithm.
    - ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens in minutes.

Functions:
    - create_access_token: Generate a new JWT access token.
    - get_current_user: Get the current authenticated user based on the provided JWT token.
    - get_user_by_name: Retrieve a user by their name from the database.

Usage:
    - Import the functions and constants as needed.
    - Use these functions for authentication and authorization in FastAPI routes.

Example:
    from api.schemas.oauth2 import oauth2_scheme
    from api.cruds.token import create_access_token, get_current_user, get_user_by_name
    from api.db import get_db
    from fastapi import Depends, FastAPI, HTTPException, status
    from sqlalchemy.ext.asyncio import AsyncSession

    app = FastAPI()

    @app.post("/token")
    async def login_for_access_token(
        auth_info: token_schema.Token, db: AsyncSession = Depends(get_db)
    ):
        user = await get_user_by_name(db=db, user_name=auth_info.username)
        password_hash = HashGenerator().hash_string(auth_info.password)
        if user.password_hash == password_hash:
            access_token = create_access_token(data={"sub": auth_info.username})
            return {
                "access_token": access_token,
                "token_type": "bearer",
            }
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    @app.get("/get-current-user", dependencies=[Depends(get_current_user)])
    async def get_current_usermodel(auth_user: user_schema.User):
        return {"message": auth_user.user_name}
"""
from datetime import datetime, timedelta
from typing import Annotated, Optional, Tuple

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine import Result
from api.models import model
import api.schemas.token as token_schema
from api.db import get_db
from api.schemas.oauth2 import oauth2_scheme

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """
    Generate a new JWT access token.

    Args:
        data (dict): Data to be encoded into the token.

    Returns:
        str: Encoded JWT access token.
    """
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)
):
    """
    Get the current authenticated user based on the provided JWT token.

    Args:
        token (Annotated[str, Depends(token_schema.oauth2_scheme)]):
            JWT token provided in the request.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        model.User: Authenticated user data.

    Raises:
        HTTPException: If authentication fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
        token_data = token_schema.TokenData(user_name=user_name)
    except JWTError as e:
        raise credentials_exception from e

    user = await get_user_by_name(db=db, user_name=token_data.user_name)

    if user is None:
        raise credentials_exception
    return user


async def get_user_by_name(db: AsyncSession, user_name: str) -> Optional[model.User]:
    """
    Retrieve a user by their name from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        user_name (str): Name of the user to retrieve.

    Returns:
        Optional[model.User]: User data if found, otherwise None.
    """
    result: Result = await db.execute(
        select(model.User).filter(model.User.user_name == user_name)
    )
    user: Optional[Tuple[model.User]] = result.first()
    return user[0] if user else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す
