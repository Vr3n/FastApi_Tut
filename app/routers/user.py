

from typing import List, Optional
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/posts', response_model=List[schemas.PostResponse])
def get_current_user_posts(db: Session = Depends(get_db), current_user: schemas.CurrentUserResponse = Depends(oauth2.get_current_user), limit:int = 10):
    user_posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).all()

    print(limit)

    return user_posts


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist.")

    return user


# @router.get('/posts', response_model=List[schemas.PostResponse])
# def get_current_user_posts(db: Session = Depends(get_db), current_user: schemas.CurrentUserResponse = Depends(oauth2.get_current_user)):
#     user_posts = db.query(models.Post).filter(
#         models.Post.owner_id.id == current_user.id)

#     return user_posts
