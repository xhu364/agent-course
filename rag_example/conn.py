import psycopg2
from pgvector.psycopg2 import register_vector


def create_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="ragdb",
        user="postgres",
        password="password",
        port=5432,
    )
    register_vector(conn)
    return conn
