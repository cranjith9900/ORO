from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from .schemas import ChatRequest
from .controller import store_chunks, search_chunks, generate_answer
from .utils import extract_pdf, extract_excel, chunk_text
from app.database import get_db

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- UPLOAD ----------
@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        text = extract_pdf(file_path)
    else:
        text = extract_excel(file_path)

    chunks = chunk_text(text)
    store_chunks(db, chunks, file.filename)

    return {"message": "File processed successfully"}


# ---------- CHAT ----------
@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    chunks = search_chunks(db, req.query)
    answer = generate_answer(req.query, chunks)

    return {
        "answer": answer,
        "context": chunks
    }