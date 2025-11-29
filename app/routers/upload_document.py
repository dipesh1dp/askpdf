from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
import os
import aiofiles
from sympy import det 

from .. import models 
from ..database import get_db 
from .. import oauth2
from ..services.document_processor import load_documents
from ..services.vector_store import add_docs_to_vector_store
from .. import schemas

router = APIRouter(
    prefix="/document", 
    tags=["Docs"]
    )

@router.post("/upload") 
async def upload_document(file: UploadFile= File(...), 
                          db: AsyncSession=Depends(get_db),
                          current_user: int=Depends(oauth2.get_current_user)
                          ): 
    # File upload validation 
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Unsupported file type. Upload PDF or TXT only."
                            )
    
    os.makedirs("uploaded_files", exist_ok=True)

    safe_filename = os.path.basename(file.filename)
    file_path = f"uploaded_files/{safe_filename}"

    # Async file save
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())

    # Process the document
    try:
        docs = load_documents(file_path)
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Document loading failed: {str(e)}"
                            )
    try:
        doc_ids = add_docs_to_vector_store(docs)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Vector store insertion failed: {str(e)}"
                            )

    # Save metadata
    new_doc = models.Document(filename=safe_filename, 
                              file_path=file_path,
                              user_id=current_user.id
                              )

    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)

    return {"filename": file.filename, "document_ids": doc_ids}


# Test endpoint
@router.post("/ping")
async def test(file: UploadFile = File(...),
               db: AsyncSession=Depends(get_db), 
               current_user: int=Depends(oauth2.get_current_user)):
    return {"filename": file.filename}
