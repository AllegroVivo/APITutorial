from typing import List, Optional

from fastapi import HTTPException, Response, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db
################################################################################

router = APIRouter(prefix="/posts", tags=["Posts"])

################################################################################
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = None):

    qbase = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    joined = qbase.join(models.Vote, models.Post.id == models.Vote.post_id)
    results = joined.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

################################################################################
@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

################################################################################
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == post_id)
    
    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"Post ID {post_id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this post")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=204)

################################################################################
@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    qbase = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    joined = qbase.join(models.Vote, models.Post.id == models.Vote.post_id)
    
    if not post:
        raise HTTPException(status_code=404, detail=f"Post ID {post_id} not found")
    
    return post

################################################################################
@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    pquery = db.query(models.Post).filter(models.Post.id == post_id)

    post_to_update = pquery.first()
    if not post_to_update:
        raise HTTPException(status_code=404, detail=f"Post ID {post_id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this post")

    pquery.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return pquery.first()

################################################################################
