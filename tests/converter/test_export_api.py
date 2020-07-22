import pytest
from unittest import mock

from pysqldump.dump import SQLDump


@pytest.fixture
def query():
    return "SELECT * FROM users LIMIT 1"


@pytest.fixture
def data():
    return {"id": 51, "username": "John Doe", "email": "john.doe@example.com"}


@mock.patch.object(SQLDump, "make_query")
def test_sql_export_should_print_data(mock_sql_response, query, data, capsys):
    mock_sql_response.return_value = data
    SQLDump(query=query, headers=["id", "username", "email"], ).make(pprint=True)
    expected = "{'id': 51, 'username': 'John Doe', 'email': 'john.doe@example.com'}\n"
    captured = capsys.readouterr()
    assert captured.out == expected
