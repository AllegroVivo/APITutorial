from datetime import datetime, timedelta, UTC

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import schemas, database, models
from .config import settings
################################################################################

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

################################################################################
def create_access_token(data: dict):
    
    to_encode = data.copy()
    
    expiry = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

################################################################################
def verify_token(token: str, credentials_exception: Exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id: str = payload.get("user_id")
        if _id is None:
            raise credentials_exception
        token_data = schemas.TokenData(_id=_id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
################################################################################
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token._id).first()
    return user

################################################################################
