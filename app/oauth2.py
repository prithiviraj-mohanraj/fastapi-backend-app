from jose import JWTError,jwt
from fastapi import HTTPException,Depends,status
from datetime import datetime,timedelta,timezone
from app.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="login")
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    enocded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return enocded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")

        # Change 'user_id' to 'id' here
        id: str = payload.get("id")  # Look for 'id' instead of 'user_id'
        
        if id is None:
            print("user_id not found in token payload")  # Debugging message
            raise credentials_exception
        
        token_data = TokenData(id=id)
        return token_data
    except JWTError as e:
        print(f"JWTError: {str(e)}")  # Log the error message
        raise credentials_exception

    
def get_current_user(token:str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token,credentials_exception)


