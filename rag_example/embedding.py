from conn import create_conn
from sentence_transformers import SentenceTransformer
from psycopg2.extras import Json


def create_embedding(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    connection = create_conn()
    cursor = connection.cursor()

    embeddings = []
    for chunk in chunks:

        vector = model.encode(chunk.page_content)
        embeddings.append(vector)
        cursor.execute(
            """
            INSERT INTO documents
                (content, metadata, embedding)
            VALUES
                (%s, %s, %s)
            """,
            (
                chunk.page_content,
                Json(chunk.metadata),
                vector,
            ),
        )
    connection.commit()
    return embeddings
