import sqlite3

import pymysql
import pytest
from pysqldump.adapters.connectors import MySQLConnector, SQLiteConnector


@pytest.mark.xfail(
    raises=pymysql.err.OperationalError, reason="Database not implemented"
)
def test_mysql_connector_payload():
    connector = MySQLConnector(config="test_config.yaml")
    assert connector.connect.host == "localhost"
    assert connector.connect.db == b"Chinook"
    assert connector.connect.user == b"root"
    assert connector.connect.password == b"password"


@pytest.mark.xfail(reason="Database not implemented")
def test_mysql_connector():
    connector = MySQLConnector(config="test_config.yaml")
    query = "SELECT EmployeeId, LastName, FirstName FROM Employee WHERE EmployeeId = 1;"
    expected = [{"EmployeeId": 1, "LastName": "Adams", "FirstName": "Andrew"}]
    result = connector.execute(query=query)
    assert result == expected


@pytest.mark.xfail(
    raises=sqlite3.OperationalError, reason="Database not implemented in pipeline"
)
def test_sqlite_connector():
    connector = SQLiteConnector(config="test_sqlite_config.yaml")
    query = "SELECT EmployeeId, LastName, FirstName FROM Employee WHERE EmployeeId = 1;"
    expected = [{"EmployeeId": 1, "LastName": "Adams", "FirstName": "Andrew"}]
    result = connector.execute(query=query)
    assert result == expected
