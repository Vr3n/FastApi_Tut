from turtle import update
from typing import Dict, Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

my_posts = []


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


def find_post(id: int) -> Post:
    post = None
    try:
        post = my_posts[id]
    except IndexError:
        post = None
    return post


@app.get("/")
def root():
    return {"message": "Hello, Friend"}


@app.get("/posts")
def get_posts():
    return my_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    my_posts.append(post)
    return {"data": "created!"}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    return {"post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    my_posts[id] = updated_post
    return {"message": "Updated Successfully", "post": updated_post}
