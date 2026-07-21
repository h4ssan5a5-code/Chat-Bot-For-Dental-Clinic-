import faiss
import numpy as np

from app.rag.loader import load_markdown_documents
from app.rag.chunker import create_chunks
from app.rag.embeddings import embed_texts


class VectorStore:

    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self):
        documents = load_markdown_documents()

        self.chunks = create_chunks(documents)

        texts = [chunk["text"] for chunk in self.chunks]

        embeddings = embed_texts(texts)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        print(f"Indexed {len(texts)} chunks.")

    def search(self, query, k=3):
        query_embedding = embed_texts([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for i, idx in enumerate(indices[0]):
            results.append({
                "text": self.chunks[idx]["text"],
                "source": self.chunks[idx]["source"],
                "distance": float(distances[0][i])
            })

        return results