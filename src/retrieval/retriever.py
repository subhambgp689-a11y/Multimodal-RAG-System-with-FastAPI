from src.retrieval.embedder import embed_texts

def retrieve(query, store):
    q_vec = embed_texts([query])
    return store.search(q_vec, k=5)