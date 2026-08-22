from __future__ import annotations

import json
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

from mcp_knowledge_server.db.connection import PostgreSQLConnectionServer


def search_documents(
	query: str,
	model: SentenceTransformer,
	top_k: int = 3,
) -> list[dict[str, Any]]:
	"""Return the most similar stored document chunks for a query."""
	if not query.strip():
		raise ValueError("query must not be empty")
	if top_k <= 0:
		raise ValueError("top_k must be greater than 0")

	query_embedding = model.encode(
		query,
		normalize_embeddings=True,
		convert_to_numpy=True,
		show_progress_bar=False,
	)

	database = PostgreSQLConnectionServer()
	with database.connection() as connection:
		with connection.cursor() as cursor:
			cursor.execute(
				"SELECT source, model, text, embedding FROM embeddings"
			)
			rows = cursor.fetchall()

	results: list[dict[str, Any]] = []
	for source, model_name, text, embedding_json in rows:
		embedding = np.asarray(json.loads(embedding_json), dtype=float)
		score = float(np.dot(query_embedding, embedding))
		results.append(
			{
				"source": source,
				"model": model_name,
				"text": text,
				"score": score,
			}
		)

	results.sort(key=lambda result: result["score"], reverse=True)
	return results[:top_k]
