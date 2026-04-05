import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add(self, vectors, docs):
        self.index.add(np.array(vectors))
        self.documents.extend(docs)

    def search(self, query_vector, k=5):
        D, I = self.index.search(query_vector, k)
        return [self.documents[i] for i in I[0]]