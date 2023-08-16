from collections import namedtuple
from datetime import datetime
from pytest import fixture
from unittest import mock
from page_analyzer.database import PostgresConnection
from page_analyzer.repository import URLChecksRepository


@fixture
@mock.patch.object(PostgresConnection, "__init__",
                   new=lambda x: None)
def checks_repo():
    repo = URLChecksRepository(PostgresConnection)
    return repo


Record = namedtuple(
    "Record",
    ["id", "url_id",
     "status_code", "h1",
     "title", "description",
     "created_at"]
)
record = Record(1, 1, 200, "Foo", "Bar", "FooBar", datetime(2023, 8, 16))


@mock.patch.object(PostgresConnection, "execute",
                   new=lambda x, y: None)
def test_add_check(checks_repo):
    assert checks_repo.add_check(
            1, 200, "Foo", "Bar", "FooBar",
            ) is None


@mock.patch.object(PostgresConnection, "execute_and_get_list",
                   new=lambda x, y: [record,])
def test_get_checks(checks_repo):
    assert checks_repo.get_checks(1) == [record, ]


@mock.patch.object(PostgresConnection, "execute_and_get_list",
                   new=lambda x, y: [record,])
def test_get_urls_with_checks(checks_repo):
    assert checks_repo.get_urls_with_checks() == [record, ]
