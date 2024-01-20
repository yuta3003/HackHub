from fastapi import FastAPI

from api.routers import post, user

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
