from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import Depends, status, HTTPException 
from fastapi.security import OAuth2PasswordBearer 
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, models, database
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from .config import settings

# Load environment variables 
SECRET_KEY = settings.secret_key 
ALGORITHM = settings.algorithm
ACESS_TOKEN_EXPIRE_MINUTES = settings.acess_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 


def create_access_token(data: dict): 
    to_encode = data.copy() 
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return encoded_jwt 


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return schemas.TokenData(id=user_id)

    except ExpiredSignatureError:
        logging.error(f"Token has expired: {token}")
        raise credentials_exception

    except JWTError as e:
        logging.error(f"JWT Error: {e}")
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme), 
                           db: AsyncSession = Depends(database.get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    stmt = select(models.User).where(models.User.id == token_data.id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")

    return user
