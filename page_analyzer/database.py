import os
from typing import NamedTuple
import psycopg2
from psycopg2.extras import NamedTupleCursor


class DataBaseConnection():
    """ Represent connection to DB """

    def __init__(self) -> None:
        """Initiate connection to Postgresql DB
           and make migrations"""

        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            cursor_factory=NamedTupleCursor
        )

        with open("database.sql", "r") as doc:
            statement = doc.read()

        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(statement)


class URLsInterface(DataBaseConnection):

    def insert_values_urls(self, *args: str) -> None:
        STATEMENT = "INSERT INTO urls (name) VALUES (%s)"

        with self.conn as conn:
            with conn.cursor() as cur:
                for name in args:
                    cur.execute(STATEMENT, (name,))

    def get_url(self, id) -> NamedTuple:
        """
        Return one url from db
        Requires url's id
        """
        STATEMENT = "SELECT * FROM urls WHERE id = %s;"
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(STATEMENT, (id,))
                url = cur.fetchone()
        return url

    def get_id_from_url(self, name: str) -> int:
        STATEMENT = "SELECT * FROM urls WHERE name = %s;"
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(STATEMENT, (name,))
                url = cur.fetchone()
        return url.id


class URLChecksInterface(DataBaseConnection):

    def create_new_check(self, url_id: int, status_code: int) -> None:
        STATEMENT = ("INSERT INTO url_checks (url_id, status_code) "
                     "VALUES (%s, %s)")

        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(STATEMENT, (url_id, status_code))

    def get_checks_for_site(self, url_id: int) -> list[NamedTuple]:
        STATEMENT = "SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC"

        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(STATEMENT, (url_id,))
                checks = cur.fetchall()
        return checks


class DB(URLChecksInterface, URLsInterface):

    def get_urls_with_checks(self) -> list[NamedTuple]:
        STATEMENT = ("SELECT DISTINCT ON (urls.id) urls.id, urls.name, "
                     "url_checks.created_at, url_checks.status_code from "
                     "urls JOIN url_checks ON url_checks.url_id = urls.id "
                     "ORDER BY id, created_at DESC;")

        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(STATEMENT)
                urls = cur.fetchall()
        return urls
