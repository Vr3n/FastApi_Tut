import os
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from typing import Dict, Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

my_posts = []


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


while True:
    try:
        conn = psycopg2.connect(
            host=os.environ.get('PG_HOST'),
            database=os.environ.get('PG_DATABASE'),
            user=os.environ.get("PG_USER"),
            password=os.environ.get('PG_PASSWORD'),
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connected Successfully!")
        break
    except Exception as err:
        print(Exception(f"Conn Failure: {err}"))
        time.sleep(5)


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
    cursor.execute("""
        SELECT * FROM post
    """)
    posts = cursor.fetchall()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """
        INSERT INTO post (title, content, published) VALUES
        (%s,%s,%s)
        RETURNING *;
    """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post, "message": "post created successfully!"}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(
        """
        SELECT * FROM post
        WHERE id=%s;
        """, str(id)
    )
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    cursor.execute(
        """
        DELETE FROM post
        WHERE id=%s
        RETURNING *;
        """,
        str(id)
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, response: Response):
    cursor.execute(
        """
        UPDATE post
        SET title=%s,
            content=%s
        WHERE id=%s
        RETURNING *;
        """, (updated_post.title, updated_post.content, str(id))
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    return {"message": "Updated Successfully", "data": updated_post}


@app.put("/posts/{id}/publish")
def publish_post(id: int, response: Response):
    published = True
    cursor.execute(
        """
        UPDATE post
        SET published=%s 
        WHERE id=%s
        RETURNING *;
        """, (published, str(id))
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    return {"message": f"Post {id} Published Successfully!", "data": post}
