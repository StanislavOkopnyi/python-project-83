from typing import NamedTuple

from page_analyzer.database import AbstractConnection


class DefaultRepository():

    def __init__(self, db_connection: AbstractConnection) -> None:
        self.db_connection = db_connection()


class URLRepository(DefaultRepository):

    def add_url(self, url: str) -> None:
        QUERY = ("INSERT INTO urls (name) VALUES (%s)", (url, ))
        self.db_connection.execute(QUERY)

    def get_id_from_url(self, name: str) -> int:
        QUERY = ("SELECT * FROM urls WHERE name = %s;", (name, ))
        url = self.db_connection.execute_and_get_item(QUERY)
        return url.id

    def get_url(self, id: int) -> NamedTuple:
        QUERY = ("SELECT * FROM urls WHERE id = %s;", (id, ))
        url = self.db_connection.execute_and_get_item(QUERY)
        return url


class URLChecksRepository(DefaultRepository):

    def add_check(
        self, url_id: int, status_code: int,
        h1: str = "", title: str = "", description: str = "",
    ) -> None:

        QUERY = (
                ("INSERT INTO url_checks (url_id, status_code, h1, "
                 "title, description) VALUES (%s, %s, %s, %s, %s)"),
                (url_id, status_code, h1, title, description)
        )
        self.db_connection.execute(QUERY)

    def get_checks(self, url_id: int) -> list[NamedTuple]:
        QUERY = ("SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC",
                 (url_id,))
        checks = self.db_connection.execute_and_get_list(QUERY)
        return checks

    def get_urls_with_checks(self) -> list[NamedTuple]:
        QUERY = (("SELECT DISTINCT ON (urls.id) urls.id, urls.name, "
                  "url_checks.created_at, url_checks.status_code from "
                  "urls JOIN url_checks ON url_checks.url_id = urls.id "
                  "ORDER BY id, created_at DESC;"), )
        urls_with_checks = self.db_connection.execute_and_get_list(QUERY)
        return urls_with_checks
