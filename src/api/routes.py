from fastapi import APIRouter, UploadFile, File
import os

from src.ingestion.pdf_parser import extract_text
from src.retrieval.embedder import embed_texts
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import retrieve
from src.models.llm import generate_answer
from src.models.vision_model import describe_image

router = APIRouter()

vector_store = None


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    global vector_store

    path = f"temp_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    texts = extract_text(path)

    embeddings = embed_texts(texts)
    vector_store = VectorStore(len(embeddings[0]))
    vector_store.add(embeddings, texts)

    return {"message": "Document ingested successfully"}


@router.post("/query")
def query(q: str):
    if vector_store is None:
        return {"error": "No document ingested"}

    docs = retrieve(q, vector_store)
    context = "\n".join(docs)

    answer = generate_answer(q, context)

    return {"answer": answer}


@router.post("/image-query")
async def image_query(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    description = describe_image(path)

    return {"description": description}