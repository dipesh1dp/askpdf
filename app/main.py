from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routers import chat, login, upload_document, user
from .database import init_db



@asynccontextmanager 
async def lifespan(app: FastAPI): 
    # Startup 
    print("Starting up...") 
    # Initalize database
    await init_db() 
    print("Ready") 
    yield 
    print("Shutting down...")


app = FastAPI(
    title= "RAG QA Chatbot API",
    description="Simple RAG based Question Answering Chatbot", 
    version="1.0.0",
    lifespan=lifespan
)



# CORS 


# Include routers 
app.include_router(login.router)
app.include_router(upload_document.router)
app.include_router(chat.router)
app.include_router(user.router)


@app.get("/") 
async def read_root():
    return {
        "message": "RAG QA Chatbot",
        "docs": "/docs"
    }
 

@app.get("/health") 
async def health(): 
    return {"status": "ok"}

