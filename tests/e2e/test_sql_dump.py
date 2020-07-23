import json
import sqlite3

import pytest
from pysqldump.dump import SQLDump

query = "SELECT EmployeeId, LastName, FirstName FROM Employee WHERE EmployeeId = 1;"


@pytest.mark.xfail(
    raises=sqlite3.OperationalError, reason="Database not implemented in pipeline"
)
def test_api():
    SQLDump(
        query=query, export_to="employee.json", config="test_sqlite_config.yaml"
    ).make()
    result = json.loads(open("employee.json").read())
    assert result == [{"EmployeeId": 1, "LastName": "Adams", "FirstName": "Andrew"}]
