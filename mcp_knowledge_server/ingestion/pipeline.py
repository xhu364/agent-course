from __future__ import annotations

from pathlib import Path

from .chunker import chunk_text
from .config import (
    CHUNK_SIZE,
    MODEL_NAME,
    OVERLAP,
    SIMILARITY_THRESHOLD,
    SOURCE_FILE,
)
from .embedder import embed_texts, load_model
from .repository import save_embeddings


def ingest(source_file: Path = SOURCE_FILE) -> Path:
    """Read, chunk, embed, and store one document."""
    if not source_file.is_file():
        raise FileNotFoundError(f"Missing source document: {source_file}")

    model = load_model()
    text = source_file.read_text(encoding="utf-8")
    chunks = chunk_text(
        text,
        model=model,
        chunk_size=CHUNK_SIZE,
        overlap=OVERLAP,
        similarity_threshold=SIMILARITY_THRESHOLD,
    )

    if not chunks:
        raise ValueError(f"No chunks were generated from {source_file}")

    print(f"Generated {len(chunks)} semantic chunks")
    embeddings = embed_texts(model, chunks)
    save_embeddings(source_file, MODEL_NAME, chunks, embeddings)
    return source_file
