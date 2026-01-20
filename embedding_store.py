from sentence_transformers import SentenceTransformer
import faiss

def build_faiss_index(chunks):
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embeddings = embedder.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return embedder, index
