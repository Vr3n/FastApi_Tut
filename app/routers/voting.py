from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2

router = APIRouter(tags=["Voting"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: schemas.CurrentUserResponse = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id)

    if vote_query.first():
        vote_query.delete(synchronize_session=False)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Vote Removed!"
        })

    new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

    db.add(new_vote)
    db.commit()
    return {
        "message": "Vote Addded!"
    }
