from app.database import get_db
from app import models,schemas
from sqlalchemy.orm import session
from fastapi import HTTPException, Depends,APIRouter,status
from app.hashing import hash_password

router=APIRouter(prefix="/users",tags=["Users"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Responseuser)

def create_user(user:schemas.UserCreate , db:session=Depends(get_db)):
    
    
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail=f"user with email  {user.email} is found already")
    
    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user_dict["password"])
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.Responseuser)
def get_user(id:int,db:session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail=f"User with id {id} not found")
    return user