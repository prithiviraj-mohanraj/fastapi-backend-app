from app.database import engine,SessionLocal,Base,get_db
from app import models,schemas,oauth2
from sqlalchemy.orm import session
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from typing import Optional,List


router=APIRouter(prefix="/vote",tags=["Vote"])


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} is not exist")
    vote_query=db.query(models.Votes).filter(
            models.Votes.post_id==vote.post_id,models.Votes.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        new_vote=models.Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully Voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted the vote"}
