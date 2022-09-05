from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, auth

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello, Friend"}


app.include_router(post.router, prefix="/posts")
app.include_router(user.router, prefix="/auth")
app.include_router(auth.router, prefix="/auth")
