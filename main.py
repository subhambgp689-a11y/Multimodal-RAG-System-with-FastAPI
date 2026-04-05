from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.routes import router, vector_store
from src.models.llm import is_llm_ready
from src.models.vision_model import is_vision_ready

app = FastAPI(title="Multimodal RAG Automotive API")

app.include_router(router)

start_time = datetime.utcnow()

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    uptime = datetime.utcnow() - start_time
    indexed_documents = vector_store.document_count() if vector_store else 0
    index_size = vector_store.index_size() if vector_store else 0
    index_memory_bytes = vector_store.index_memory_bytes() if vector_store else 0

    return {
        "status": "ok",
        "model_readiness": {
            "llm": is_llm_ready(),
            "vision": is_vision_ready(),
        },
        "indexed_documents": indexed_documents,
        "index_size": index_size,
        "index_memory_bytes": index_memory_bytes,
        "uptime_seconds": int(uptime.total_seconds()),
        "uptime": str(uptime),
    }
