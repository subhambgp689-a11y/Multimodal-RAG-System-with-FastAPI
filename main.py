from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Multimodal RAG Automotive API")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}