"""PostgreSQL connection management for the local Docker database."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Iterator

import psycopg
from psycopg import Connection


class PostgreSQLConnectionServer:
    """Manage connections to a PostgreSQL database.

    Connection settings default to the conventional local Docker PostgreSQL
    values and can be overridden with these environment variables:

    - POSTGRES_HOST
    - POSTGRES_PORT
    - POSTGRES_DB
    - POSTGRES_USER
    - POSTGRES_PASSWORD

    Example:

        database = PostgreSQLConnectionServer()
        connection = database.connect()

        try:
            connection.execute("SELECT 1")
            connection.commit()
        finally:
            connection.close()
    """

    def __init__(
        self,
        host: str | None = None,
        port: int | str | None = None,
        database: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ) -> None:
        """Initialize PostgreSQL connection settings."""

        self.connection_info: dict[str, Any] = {
            "host": host or os.getenv("POSTGRES_HOST", "localhost"),
            "port": port or os.getenv("POSTGRES_PORT", "5432"),
            "dbname": database or os.getenv("POSTGRES_DB", "appdb"),
            "user": user or os.getenv("POSTGRES_USER", "post_user"),
            "password": password
            or os.getenv(
                "POSTGRES_PASSWORD",
                "password1234",
            ),
        }

    def connect(self) -> Connection[Any]:
        """Open and return a new PostgreSQL connection."""
        return psycopg.connect(**self.connection_info)

    @contextmanager
    def connection(self) -> Iterator[Connection[Any]]:
        """Provide a connection and manage its transaction.

        The transaction is committed when the context exits successfully.
        If an exception occurs, the transaction is rolled back and the
        exception is re-raised.
        """
        connection = self.connect()

        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def health_check(self) -> bool:
        """Return True if PostgreSQL accepts connections."""
        try:
            with self.connection() as connection:
                connection.execute("SELECT 1")
            return True
        except psycopg.Error:
            return False


if __name__ == "__main__":
    database = PostgreSQLConnectionServer()

    if database.health_check():
        print("PostgreSQL connection successful.")
    else:
        print("PostgreSQL connection failed.")
