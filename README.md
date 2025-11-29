# AskPDF

A lightweight, modular Retrieval-Augmented Generation (RAG) backend built with **FastAPI**, **FAISS**, **LangGraph**, **PostgreSQL**, and **JWT authentication**.
Supports **PDF and TXT uploads**, including **OCR extraction via Tesseract**.

---

## Features

* Asynchronous FastAPI backend with clean modular architecture and dependency injection
* FAISS vector store for efficient similarity search
* LangGraph agent pipeline for orchestrating RAG steps
* RecursiveCharacterTextSplitter from LangChain for chunking documents
* PostgreSQL as the primary database
* JWT-based authentication & user management
* Document upload support (PDF, TXT)
* Tesseract OCR for extracting text from scanned PDFs
* Simple and extendable service layer design

---

## Project Structure

```
app/
│
├── routers/
│   ├── chat.py
│   ├── login.py
│   ├── upload_document.py
│   └── user.py
│
├── services/
│   ├── document_processor.py
│   ├── langgraph_agent.py
│   └── vector_store.py
│
├── config.py
├── database.py
├── main.py
├── models.py
├── oauth2.py
├── schemas.py
├── utils.py
├── README.md
└── requirements.txt
```

---

## Core Components

### **1. Document Processing**

* Handles PDF/TXT upload
* Uses Tesseract OCR when PDF contains images
* Extracted text is chunked using LangChain RecursiveCharacterTextSplitter for optimal RAG performance

### **2. Vector Store**

* Uses FAISS for fast approximate nearest-neighbor search
* Stores embeddings for all uploaded documents

### **3. LangGraph Agent**

* Manages RAG workflow
* Defines retrieval → reasoning → response generation graph
* Uses LangGraph MemorySaver for storing intermediate state per user
* Each user session uses user_id as the thread identifier, ensuring isolated and persistent RAG state per user

### **4. Authentication**

* JWT tokens for secure login
* Includes user registration & login routes

### **5. Database**

* PostgreSQL
* SQLAlchemy ORM models
* Stores users, documents, and metadata

---

## Running the Project

### 1. Clone the repository
    
        git clone https://github.com/dipesh1dp/askpdf.git
        cd askpdf
    

### 2. Create & activate a virtual environment (recommended)
    
        python -m venv venv
        source venv/bin/activate     # macOS / Linux
        venv\Scripts\activate        # Windows
    

### 3. Install dependencies

    
        pip install -r requirements.txt


### 4. Run FastAPI

        uvicorn app.main:app --reload



### 5. Visit API docs:
        [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Uploading Documents

The `/upload` endpoint accepts:

* `.pdf` (text or scanned)
* `.txt`

Automatic OCR runs for image-based PDFs using Tesseract.

---

## Authentication

* `/register` → create user
* `/login` → get JWT token
* Protected routes require:
  `Authorization: Bearer <token>`

---

## RAG Pipeline

1. Upload → process → chunk
2. Embed chunks
3. Store embeddings in FAISS
4. LangGraph agent retrieves & generates answers

---

## Notes

* Modify `langgraph_agent.py` to customize your chain
* Replace FAISS with another store if needed
* Great base project for expanding into full RAG applications

---

## License

MIT License
