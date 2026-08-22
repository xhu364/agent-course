from sentence_transformers import SentenceTransformer

from .config import MODEL_NAME


def load_model(model_name: str = MODEL_NAME) -> SentenceTransformer:
    """Load the configured sentence-embedding model."""
    return SentenceTransformer(model_name)


def embed_texts(model: SentenceTransformer, texts: list[str]) -> list[list[float]]:
    """Generate normalized embeddings for a collection of texts."""
    return model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True,
    ).tolist()