from fastapi import Depends,HTTPException,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from app.database import get_db
from app.oauth2 import create_access_token
from app import models,schemas
from app.hashing import verify_password

router=APIRouter(tags=["Authentication"])


@router.post("/login",response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends() , db:session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    if not verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    token=create_access_token({"id":user.id})
    return {"access_token":token,"token_type":"bearer"}

