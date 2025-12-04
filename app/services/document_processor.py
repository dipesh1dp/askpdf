import fitz 
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from langchain_core.documents import Document
from ..config import settings


def extract_pdf_text(file_path: str) -> list[Document]:
    """Extract text from a PDF using PyMuPDF"""
    doc = fitz.open(file_path)
    documents = []

    for i, page in enumerate(doc):
        text = page.get_text("text")
        documents.append(
            Document(
                page_content=text,
                metadata={"source": file_path, "page": i + 1}
            )
        )
    return documents


def extract_pdf_ocr(file_path: str) -> list[Document]:
    """Extract text from a scanned PDF using OCR"""
    print("OCR: Processing scanned PDF...")
    images = convert_from_path(file_path, poppler_path=settings.poppler_path)

    documents = []
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        documents.append(
            Document(
                page_content=text,
                metadata={"source": file_path, "page": i + 1}
            )
        )
    return documents


def process_pdf(file_path: str) -> list[Document]:
    """Handle PDF processing with fallback to OCR if needed"""
    try:
        docs = extract_pdf_text(file_path)

        # If all pages are empty → scanned pdf → OCR
        if all(len(doc.page_content.strip()) == 0 for doc in docs):
            raise ValueError("No text found in PDF, switching to OCR")

        return docs

    except Exception:
        return extract_pdf_ocr(file_path)


def process_txt(file_path: str) -> list[Document]:
    """Process TXT files"""
    print(f"Processing TXT: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return [
        Document(
            page_content=text,
            metadata={"source": file_path}
        )
    ]


def process_document(file_path: str) -> list[Document]:
    """Process a document based on its file type"""
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return process_pdf(file_path)

    if ext == ".txt":
        return process_txt(file_path)

    raise ValueError(f"Unsupported file type: {ext}")


def load_documents(file_path: str) -> list[Document]:
    """Load and process a document based on its type"""
    return process_document(file_path)
