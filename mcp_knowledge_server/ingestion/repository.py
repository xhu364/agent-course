from __future__ import annotations

import json
from pathlib import Path

from mcp_knowledge_server.db.connection import PostgreSQLConnectionServer


def save_embeddings(
    source_file: Path,
    model_name: str,
    chunks: list[str],
    embeddings: list[list[float]],
) -> None:
    """Replace the stored embeddings for one source document."""
    database = PostgreSQLConnectionServer()

    with database.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY,
                    source TEXT NOT NULL,
                    model TEXT NOT NULL,
                    text TEXT NOT NULL,
                    embedding TEXT NOT NULL
                )
                """)
            cursor.execute(
                "DELETE FROM embeddings WHERE source = %s",
                (str(source_file),),
            )

            rows = [
                (
                    index,
                    str(source_file),
                    model_name,
                    chunk,
                    json.dumps(embedding),
                )
                for index, (chunk, embedding) in enumerate(zip(chunks, embeddings))
            ]
            cursor.executemany(
                """
                INSERT INTO embeddings (id, source, model, text, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                rows,
            )