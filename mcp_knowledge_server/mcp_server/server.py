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


@mcp.prompt()
def summarize_documents(topic: str) -> str:
    """Create a prompt for summarizing documents about a topic."""
    return f"""
Summarize the available documents about "{topic}".

Focus on:
1. The main ideas
2. Important facts and evidence
3. Areas where the documents disagree
4. Gaps or uncertainties

Use the retrieved documents as the primary source.
""".strip()


@mcp.prompt()
def answer_question(question: str) -> str:
    """Create a prompt for answering a question using retrieved documents."""
    return f"""
Answer this question using the retrieved documents as your primary source:

{question}

Clearly distinguish information supported by the documents
from information that is uncertain or not found.
""".strip()


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )
