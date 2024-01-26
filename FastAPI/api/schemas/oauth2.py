"""
OAuth2 Password Bearer Module.

This module defines an OAuth2 password bearer scheme for FastAPI.

Classes:
    - OAuth2PasswordBearer: OAuth2 password bearer scheme.

Usage:
    - Import the 'OAuth2PasswordBearer' class.
    - Create an instance of 'OAuth2PasswordBearer' with the 'tokenUrl' parameter.

Example:
    from fastapi.security import OAuth2PasswordBearer

    # Create an OAuth2PasswordBearer instance with the token URL
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    # Use the 'oauth2_scheme' instance in your FastAPI routes
    @app.post("/login")
    async def login(token: str = Depends(oauth2_scheme)):
        # Your authentication logic here
"""
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
