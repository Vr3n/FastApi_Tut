
from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""
    #     SELECT * FROM post
    # """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: schemas.CurrentUserResponse = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
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
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.CurrentUserResponse = Depends(oauth2.get_current_user)):
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


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db), current_user: schemas.CurrentUserResponse = Depends(oauth2.get_current_user)):
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
    return post


@router.patch("/{id}/publish", response_model=schemas.PostResponse)
def publish_post(id: int, db: Session = Depends(get_db), current_user: schemas.CurrentUserResponse = Depends(oauth2.get_current_user)):
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
    db.commit()
    db.refresh(post)
    return post
