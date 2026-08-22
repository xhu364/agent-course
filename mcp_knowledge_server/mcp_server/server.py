from mcp.server import MCPServer
from sentence_transformers import SentenceTransformer

from mcp_knowledge_server.ingestion.config import MODEL_NAME
from mcp_knowledge_server.retrieval.retriever import (
    search_documents as retrieve_documents,
)

mcp = MCPServer("knowledge-server")
_model = SentenceTransformer(MODEL_NAME)


@mcp.tool()
def search_documents(query: str, top_k: int = 3):
    """Search indexed document chunks by semantic similarity."""
    return retrieve_documents(query=query, model=_model, top_k=top_k)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )
