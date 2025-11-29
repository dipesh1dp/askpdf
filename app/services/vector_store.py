import faiss
from typing import List
from fastapi import HTTPException, status
from grpc import Status
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from sympy import det

from .. config import settings 

# Initialize embedding model 
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", 
                                            encode_kwargs={"normalize_embeddings": True}
)

# Initialize FAISS index 
embedding_dim = len(embedding_model.embed_query("Hello world")) 
index = faiss.IndexFlatL2(embedding_dim) 

vector_store = FAISS(
    embedding_function=embedding_model, 
    index=index, 
    docstore=InMemoryDocstore(), 
    index_to_docstore_id={}
)

# Chunking and adding documents to vector store 
def add_docs_to_vector_store(docs: list[Document], 
                             chunk_size: int = settings.chunk_size,
                             chunk_overlap: int = settings.chunk_overlap):
    """Split -> Embed -> Add to vector store"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""], 
        add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs) 
    try: 
        doc_ids = vector_store.add_documents(all_splits) 
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Error with Vector Store: {str(e)}")
    return doc_ids 

