from fastapi import HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db
################################################################################

router = APIRouter(prefix="/vote", tags=["Voting"])

################################################################################
@router.post("/", status_code=201, response_model=schemas.Vote)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post ID {vote.post_id} not found")
    
    vquery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found = vquery.first()
    if vote.direction == 1:
        if found:
            raise HTTPException(status_code=409, detail="You have already upvoted this post")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote!"}
    else:
        if not found:
            raise HTTPException(status_code=404, detail="You have not upvoted this post")
        vquery.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully removed vote!"}

################################################################################
