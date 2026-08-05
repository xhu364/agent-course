from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedding import create_embedding

BASE_DIR = Path(__file__).parent

file_path = BASE_DIR / "company_policy.txt"

loader = TextLoader(str(file_path), encoding="utf-8")


splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)


chunks = splitter.split_documents(loader.load())

from sentence_transformers import SentenceTransformer

embeddings = create_embedding(chunks)

query = "What is the company vacation policy?"

model = SentenceTransformer("all-MiniLM-L6-v2")
query_vector = model.encode(query)

print(len(query_vector))

from conn import create_conn


def search_documents(query, top_k=5):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_vector = model.encode(query)

    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            content,
            metadata,
            1 - (embedding <=> %s) AS similarity
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT %s
        """,
        (query_vector, query_vector, top_k),
    )

    return cursor.fetchall()


query = "Attendance issues include"
result = search_documents(query, 2)
print(query)
print(result[-1])
