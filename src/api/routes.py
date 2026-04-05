from fastapi import APIRouter, UploadFile, File, Form, Body, HTTPException
import os
import logging
import traceback
from openai import RateLimitError, APIError

from src.ingestion.pdf_parser import extract_text
from src.ingestion.table_extractor import extract_tables
from src.retrieval.embedder import embed_texts
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import retrieve
from src.models.llm import generate_answer
from src.models.vision_model import describe_image

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


router = APIRouter()

vector_store = None


def _format_table_as_markdown(table, title=None):
    if not table:
        return ""

    clean_row = lambda row: [cell.strip() if isinstance(cell, str) else "" for cell in row]
    rows = [clean_row(row) for row in table if row]
    if not rows:
        return ""

    header = rows[0]
    separator = ["---" for _ in header]
    body = rows[1:]

    lines = []
    if title:
        lines.append(title)
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(separator) + " |")
    for row in body:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    global vector_store

    try:
        path = f"temp_{file.filename}"

        with open(path, "wb") as f:
            f.write(await file.read())

        texts = extract_text(path)
        tables = extract_tables(path)
        os.remove(path)

        table_texts = []
        for idx, table in enumerate(tables, start=1):
            markdown_table = _format_table_as_markdown(table, title=f"Table {idx}:")
            if markdown_table:
                table_texts.append(markdown_table)

        all_texts = texts + table_texts
        embeddings = embed_texts(all_texts)
        vector_store = VectorStore(len(embeddings[0]))
        vector_store.add(embeddings, all_texts)

        return {"message": "Document ingested successfully"}
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        logger.error(f"Ingest error: {error_msg}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
def query(q: str = Body(...)):
    if vector_store is None:
        raise HTTPException(status_code=400, detail="No document ingested")

    try:
        docs = retrieve(q, vector_store)
        if not docs:
            raise HTTPException(status_code=404, detail="No relevant documents found for the query")

        context = "\n".join(docs)
        answer = generate_answer(q, context)

        return {"answer": answer}
    except HTTPException:
        raise
    except RateLimitError as e:
        error_msg = f"RateLimitError: {str(e)}\n{traceback.format_exc()}"
        logger.error(f"Query error: {error_msg}")
        raise HTTPException(status_code=429, detail="OpenAI API quota exceeded. Please check your account billing and quota limits at https://platform.openai.com/account/billing/overview")
    except APIError as e:
        error_msg = f"APIError: {str(e)}\n{traceback.format_exc()}"
        logger.error(f"Query error: {error_msg}")
        raise HTTPException(status_code=503, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        logger.error(f"Query error: {error_msg}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image-query")
async def image_query(file: UploadFile = File(...), q: str | None = Form(None)):
    try:
        path = f"temp_{file.filename}"

        with open(path, "wb") as f:
            f.write(await file.read())

        description = describe_image(path)
        os.remove(path)

        if q:
            prompt = f"Image description: {description}\n\nQuestion: {q}"
            answer = generate_answer(q, prompt)
            return {"description": description, "answer": answer}

        return {
            "description": description,
            "message": "To ask a question about this image, send the image with a form field named 'q'."
        }
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        logger.error(f"Image query error: {error_msg}")
        raise HTTPException(status_code=500, detail=str(e))
