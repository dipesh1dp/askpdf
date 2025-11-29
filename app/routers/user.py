from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from .. import models, schemas, utils 
from ..database import get_db


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
) 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User) 
async def create_user(user: schemas.UserCreate, db: AsyncSession=Depends(get_db)): 
    # has the password 
    hashed_password = utils.hash(user.password) 
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) 
    db.add(new_user) 
    
    await db.commit()
    await db.refresh(new_user) 
    return new_user 

