from collections import namedtuple
from datetime import datetime
from pytest import fixture

from page_analyzer.database import PostgresConnection
from page_analyzer.repository import URLChecksRepository


@fixture
def checks_repo(mocker):
    repo = URLChecksRepository(PostgresConnection)
    return repo


@fixture
def record():
    Record = namedtuple(
            "Record",
            ["id", "url_id",
             "status_code", "h1",
             "title", "description",
             "created_at"]
            )
    return Record(1, 1, 200, "Foo", "Bar", "FooBar", datetime(2023, 8, 16))


def test_add_check(mocker, checks_repo):
    mocker.patch("page_analyzer.database.PostgresConnection.__init__",
                 lambda x: None)
    mocker.patch("page_analyzer.database.PostgresConnection.execute",
                 lambda x, y: None)

    assert checks_repo.add_check(
            1, 200, "Foo", "Bar", "FooBar",
            ) is None


def test_get_checks(mocker, checks_repo, record):
    mocker.patch("page_analyzer.database.PostgresConnection.__init__",
                 lambda x: None)
    mocker.patch(
            "page_analyzer.database.PostgresConnection.execute_and_get_list",
            lambda x, y: [record,])

    assert checks_repo.get_checks(1) == [record, ]


def test_get_urls_with_checks(mocker, checks_repo, record):
    mocker.patch("page_analyzer.database.PostgresConnection.__init__",
                 lambda x: None)
    mocker.patch(
            "page_analyzer.database.PostgresConnection.execute_and_get_list",
            lambda x, y: [record,])

    assert checks_repo.get_urls_with_checks() == [record, ]
