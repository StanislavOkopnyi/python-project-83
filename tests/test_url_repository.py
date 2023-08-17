from collections import namedtuple
from datetime import datetime
from unittest.mock import patch
from pytest import fixture

from page_analyzer.database import PostgresConnection
from page_analyzer.repository import URLRepository


@fixture
def url_repo():
    repo = URLRepository(PostgresConnection)
    return repo


Record = namedtuple(
        "Record",
        ["id", "name", "created_at"]
        )
record = Record(1, "https://google.com", datetime(2023, 8, 16))


@patch.object(PostgresConnection, "execute",
              lambda x, y: None)
@patch.object(PostgresConnection, "__init__",
              new=lambda x: None)
def test_add(url_repo):
    assert url_repo.add_url("https://google.com") is None


@patch.object(PostgresConnection, "execute_and_get_item",
              lambda x, y: record)
@patch.object(PostgresConnection, "__init__",
              new=lambda x: None)
def test_get_url(url_repo):
    assert url_repo.get_url("https://google.com") == record


@patch.object(PostgresConnection, "execute_and_get_item",
              lambda x, y: record)
@patch.object(PostgresConnection, "__init__",
              new=lambda x: None)
def test_get_id_from_url(url_repo):
    assert url_repo.get_id_from_url("https://google.com") == 1
