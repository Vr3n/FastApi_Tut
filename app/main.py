from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


# while True:
#     try:
#         conn = psycopg2.connect(
#             host=os.environ.get('PG_HOST'),
#             database=os.environ.get('PG_DATABASE'),
#             user=os.environ.get("PG_USER"),
#             password=os.environ.get('PG_PASSWORD'),
#             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connected Successfully!")
#         break
#     except Exception as err:
#         print(Exception(f"Conn Failure: {err}"))
#         time.sleep(5)


@app.get("/")
def root():
    return {"message": "Hello, Friend"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""
    #     SELECT * FROM post
    # """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     INSERT INTO post (title, content, published) VALUES
    #     (%s,%s,%s)
    #     RETURNING *;
    # """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post, "message": "post created successfully!"}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     SELECT * FROM post
    #     WHERE id=%s;
    #     """, str(id)
    # )
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     DELETE FROM post
    #     WHERE id=%s
    #     RETURNING *;
    #     """,
    #     str(id)
    # )
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     UPDATE post
    #     SET title=%s,
    #         content=%s
    #     WHERE id=%s
    #     RETURNING *;
    #     """, (updated_post.title, updated_post.content, str(id))
    # )
    # post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")
    post_query.update(updated_post.dict())
    db.commit()
    db.refresh(post)
    return {"message": "Updated Successfully", "data": post}


@app.patch("/posts/{id}/publish")
def publish_post(id: int, db: Session = Depends(get_db)):
    published = True
    # cursor.execute(
    #     """
    #     UPDATE post
    #     SET published=%s
    #     WHERE id=%s
    #     RETURNING *;
    #     """, (published, str(id))
    # )
    # post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist.")

    post_query.update({'title': post.title, 'content': post.content,
                      "published": published})

    return {"message": f"Post {id} Published Successfully!", "data": post}


@app.post('/auth/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/auth/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist.")

    return user
