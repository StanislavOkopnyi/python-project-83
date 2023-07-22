import os
from typing import NamedTuple
import psycopg2
from psycopg2.extras import NamedTupleCursor


class DB():
    """ Represent connection to DB """

    def __init__(self) -> None:
        """Initiate connection to Postgresql DB
           and create new table urls if not exist"""

        with open("database.sql", "r") as doc:
            statement = doc.read()
        with self.conn.cursor() as cur:
            cur.execute(statement)

    @property
    def conn(self):
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            cursor_factory=NamedTupleCursor
        )

    def insert_values_urls(self, *args: str) -> None:
        conn = self.conn
        with conn.cursor() as cur:
            for name in args:
                cur.execute("INSERT INTO urls (name) VALUES (%s)", (name,))
        conn.commit()

    def get_all_urls(self) -> list[NamedTuple]:
        """
        Returns all urls from db
        """
        STATEMENT = "SELECT * FROM urls ORDER BY id;"
        with self.conn.cursor() as cur:
            cur.execute(STATEMENT)
            urls = cur.fetchall()
        return urls

    def get_url(self, id) -> tuple | None:
        """
        Return one url from db
        Requires url's id
        """
        STATEMENT = "SELECT * FROM urls WHERE id = %s;"
        with self.conn.cursor() as cur:
            cur.execute(STATEMENT, (id,))
            url = cur.fetchone()
        return url
