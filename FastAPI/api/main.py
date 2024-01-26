"""
Main FastAPI application module.

This module sets up a FastAPI application and includes routers for user, post, and token.
"""

from fastapi import FastAPI

from api.routers import post, token, user

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(token.router)
