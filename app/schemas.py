from pydantic import BaseModel, EmailStr, ConfigDict 
from datetime import datetime 
from typing import List, Optional 

# User Schemas
class UserCreate(BaseModel): 
    email: EmailStr 
    username: str
    password: str 

class UserLogin(BaseModel): 
    username: str
    password: str 

class User(BaseModel): 
    id: int 
    email: EmailStr 
    username: str
    created_at: datetime 
    model_config = ConfigDict(from_attributes=True)

# Token
class Token(BaseModel): 
    access_token: str 
    token_type: str = "bearer"

class TokenData(BaseModel): 
    id: Optional[int] = None


# Document Shemas 
class DocumentOut(BaseModel): 
    filename: str 
    document_ids: list
    

# Chat Schemas 
class ChatRequest(BaseModel): 
    query: str 

class ChatResponse(BaseModel): 
    response: str


