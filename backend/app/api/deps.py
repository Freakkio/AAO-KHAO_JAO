from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from app.core.config import settings
from app.db.database import user_collection
from app.models.user import UserInDB
from app.schemas.user import TokenData, UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = user_collection.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
        
    user_model = UserInDB(**user)
    
    return UserOut(username=user_model.username, email=user_model.email, profile=user_model.profile)