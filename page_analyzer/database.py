import os
from typing import NamedTuple
from psycopg2.extras import NamedTupleCursor
from psycopg2.pool import SimpleConnectionPool
from abc import ABC, abstractmethod


class AbstractConnection(ABC):

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def execute(self, query):
        ...

    @abstractmethod
    def execute_and_get_item(self, query) -> NamedTuple:
        ...

    @abstractmethod
    def execute_and_get_list(self, query) -> list[NamedTuple]:
        ...


class PostgresConnection(AbstractConnection):
    """ Represent connection to DB """

    def __init__(self) -> None:
        super().__init__()
        """Initiate connection to Postgresql DB
           and make migrations"""
        DATABASE_URL = os.getenv('DATABASE_URL')

        self._pool = SimpleConnectionPool(
            1, 20,
            DATABASE_URL,
            cursor_factory=NamedTupleCursor
        )

        with open("database.sql", "r") as doc:
            query = doc.read()

        with self._pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(query)

    def execute(self, query) -> None:
        """
        Execute SQL query
        """
        with self._pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(*query)

    def execute_and_get_item(self, query) -> NamedTuple:
        """
        Execute SQL query
        Returns item
        """
        with self._pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(*query)
                result = cur.fetchone()

        return result

    def execute_and_get_list(self, query) -> list[NamedTuple]:
        """
        Execute SQL query
        Returns list of items
        """

        with self._pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(*query)
                result = cur.fetchall()

        return result
