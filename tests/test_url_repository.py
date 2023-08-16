from collections import namedtuple
from datetime import datetime
from pytest import fixture

from page_analyzer.database import PostgresConnection
from page_analyzer.repository import URLRepository


@fixture
def url_repo(mocker):
    repo = URLRepository(PostgresConnection)
    return repo


@fixture
def record():
    Record = namedtuple(
            "Record",
            ["id", "name", "created_at"]
            )
    return Record(1, "https://google.com", datetime(2023, 8, 16))


def test_add(mocker, url_repo):
    mocker.patch("page_analyzer.database.PostgresConnection.__init__",
                 lambda x: None)
    mocker.patch("page_analyzer.database.PostgresConnection.execute",
                 lambda x, y: None)

    assert url_repo.add_url("https://google.com") is None


def test_get_url(mocker, url_repo, record):
    mocker.patch("page_analyzer.database.PostgresConnection.__init__",
                 lambda x: None)
    mocker.patch(
            "page_analyzer.database.PostgresConnection.execute_and_get_item",
            lambda x, y: record)

    assert url_repo.get_url("https://google.com") == record


def test_get_id_from_url(mocker, url_repo, record):
    mocker.patch("page_analyzer.database.PostgresConnection.__init__",
                 lambda x: None)
    mocker.patch(
            "page_analyzer.database.PostgresConnection.execute_and_get_item",
            lambda x, y: record)

    assert url_repo.get_id_from_url("https://google.com") == 1
