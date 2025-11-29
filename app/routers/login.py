from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"]) 

@router.post("/login", response_model=schemas.Token) 
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)): 
    """
    Login endpoint.
    """
    # Fetch the user from the database
    stmt = select(models.User).filter(models.User.username == user_credentials.username) 
    result = await db.execute(stmt) 
    user = result.scalar_one_or_none() 
    
    # Check if user exists
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Invalid Credentials") 
    # Verify the password
    if not utils.verify(user_credentials.password, user.password): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Invalid Credentials") 
    
    # Create and return token
    access_token = oauth2.create_access_token(data={"user_id": user.id}) 
    return {"access_token": access_token, "token_type": "bearer"}
    