from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from .config import CHUNK_SIZE, OVERLAP, SIMILARITY_THRESHOLD
from .split_sentences import split_sentences


def chunk_text(
    text: str,
    model: SentenceTransformer,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
    similarity_threshold: float = SIMILARITY_THRESHOLD,
) -> list[str]:
    """Create semantically coherent chunks using sentence embeddings."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    if not 0 < similarity_threshold <= 1:
        raise ValueError("similarity_threshold must be between 0 and 1")

    sentences = split_sentences(text)
    if not sentences:
        return []

    embeddings = model.encode(
        sentences,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    chunks: list[str] = []
    current_sentences: list[str] = []
    current_embeddings: list[np.ndarray] = []
    current_length = 0

    def add_sentence(sentence: str, embedding: np.ndarray) -> None:
        nonlocal current_length

        if current_sentences:
            current_length += 1
        current_sentences.append(sentence)
        current_embeddings.append(embedding)
        current_length += len(sentence)

    def flush_chunk() -> None:
        nonlocal current_sentences
        nonlocal current_embeddings
        nonlocal current_length

        if not current_sentences:
            return

        chunk = " ".join(current_sentences).strip()
        if chunk:
            chunks.append(chunk)

        if overlap > 0:
            overlap_sentences: list[str] = []
            overlap_embeddings: list[np.ndarray] = []
            overlap_length = 0
            for sentence, embedding in zip(
                reversed(current_sentences), reversed(current_embeddings)
            ):
                if len(sentence) + overlap_length + 1 > overlap:
                    break
                overlap_sentences.insert(0, sentence)
                overlap_embeddings.insert(0, embedding)
                overlap_length += len(sentence)
                if len(overlap_sentences) > 1:
                    overlap_length += 1
            current_sentences = overlap_sentences
            current_embeddings = overlap_embeddings
            current_length = sum(len(item) for item in current_sentences) + max(
                0, len(current_sentences) - 1
            )
        else:
            current_sentences = []
            current_embeddings = []
            current_length = 0

    for sentence, embedding in zip(sentences, embeddings):
        sentence_length = len(sentence)

        if sentence_length > chunk_size:
            flush_chunk()
            tail_part = ""
            for start in range(0, sentence_length, chunk_size - overlap):
                part = sentence[start : start + chunk_size].strip()
                if part:
                    chunks.append(part)
                    tail_part = part
            if tail_part:
                chunks.pop()
                tail_embedding = model.encode(
                    tail_part,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )
                current_sentences = [tail_part]
                current_embeddings = [tail_embedding]
                current_length = len(tail_part)
            continue

        if not current_sentences:
            add_sentence(sentence, embedding)
            continue

        chunk_embedding = np.mean(current_embeddings, axis=0)
        chunk_norm = np.linalg.norm(chunk_embedding)
        if chunk_norm > 0:
            chunk_embedding = chunk_embedding / chunk_norm

        similarity_score = np.dot(chunk_embedding, embedding)
        would_exceed_size = current_length + 1 + sentence_length > chunk_size
        is_semantic_break = similarity_score < similarity_threshold

        if would_exceed_size or is_semantic_break:
            flush_chunk()
            add_sentence(sentence, embedding)
        else:
            add_sentence(sentence, embedding)

    flush_chunk()
    return chunks
