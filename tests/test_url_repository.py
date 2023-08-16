from collections import namedtuple
from datetime import datetime
from unittest.mock import patch
from pytest import fixture

from page_analyzer.database import PostgresConnection
from page_analyzer.repository import URLRepository


@fixture
def url_repo(mocker):
    mocker.patch("page_analyzer.database.PostgresConnection.__init__",
                 lambda x: None)
    repo = URLRepository(PostgresConnection)
    return repo


Record = namedtuple(
        "Record",
        ["id", "name", "created_at"]
        )
record = Record(1, "https://google.com", datetime(2023, 8, 16))


@patch.object(PostgresConnection, "execute",
              lambda x, y: None)
def test_add(url_repo):
    assert url_repo.add_url("https://google.com") is None


@patch.object(PostgresConnection, "execute_and_get_item",
              lambda x, y: record)
def test_get_url(url_repo):
    assert url_repo.get_url("https://google.com") == record


@patch.object(PostgresConnection, "execute_and_get_item",
              lambda x, y: record)
def test_get_id_from_url(url_repo):
    assert url_repo.get_id_from_url("https://google.com") == 1
