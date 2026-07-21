from sentence_transformers import SentenceTransformer

# Load once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    """
    Convert a list of strings into embedding vectors.
    """
    return model.encode(texts, convert_to_numpy=True)