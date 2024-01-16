from fastapi import FastAPI

from api.routers import user
from api.routers import post

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
