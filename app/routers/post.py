from app.database import get_db
from app import models,schemas,oauth2
from sqlalchemy.orm import session
from fastapi import Response, status, HTTPException, Depends,APIRouter
from typing import Optional
from sqlalchemy import func

router=APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
              limit: int =5,skip:int = 0,search:Optional[str]=""):
    post=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Post.id==models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return post

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
def create_post(payload: schemas.PostCreate, db: session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    new_post= models.Post(owner_id=current_user.id,**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Post.id==models.Votes.post_id,isouter=True).group_by(models.Post.id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    deleted_post=post_query.first()
    
    if deleted_post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not autorised to perform requested action" )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.PostCreate, db: session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    query_post=db.query(models.Post).filter(models.Post.id==id)
    updated_post=query_post.first()
    
    if updated_post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not autorised to perform requested action" )
    query_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    db.refresh(updated_post)
    return  updated_post
