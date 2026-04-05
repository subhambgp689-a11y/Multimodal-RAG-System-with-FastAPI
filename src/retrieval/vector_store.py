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

    def document_count(self):
        return len(self.documents)

    def index_size(self):
        return int(self.index.ntotal)

    def index_memory_bytes(self):
        if hasattr(self.index, 'd'):
            return int(self.index.ntotal * self.index.d * 4)
        return 0
