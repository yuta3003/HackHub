from fastapi import FastAPI

from api.routers import post, token, user

app = FastAPI()
app.include_router(post.router)
app.include_router(token.router)
app.include_router(user.router)
