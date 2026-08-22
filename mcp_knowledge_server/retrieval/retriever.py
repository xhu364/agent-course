from __future__ import annotations

from typing import Any

from sentence_transformers import SentenceTransformer

from mcp_knowledge_server.db.connection import PostgreSQLConnectionServer

from pgvector.psycopg import register_vector
from pgvector import Vector


def search_documents(
    query: str,
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """
    Search indexed document chunks by semantic similarity.

    The query is embedded once. PostgreSQL + pgvector performs the
    similarity search, so stored embeddings are never fetched into Python.
    """

    if not query.strip():
        raise ValueError("query must not be empty")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    # Create exactly ONE embedding for the query.
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    query_vector = query_embedding.tolist()

    database = PostgreSQLConnectionServer()

    with database.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    source,
                    model,
                    text,
                    embedding <=> %s::vector AS distance
                FROM embeddings
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    query_vector,
                    query_vector,
                    top_k,
                ),
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "source": row[1],
            "model": row[2],
            "text": row[3],
            "distance": float(row[4]),
        }
        for row in rows
    ]
