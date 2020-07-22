from typing import List, Optional

from pysqldump.adapters.connector import MySQLConnector
from pysqldump.domain.manager import OutputManager
from pysqldump.query import Query


class SQLDump:
    def __init__(
        self, query: (Query, str), headers: List[str] = None, export_to: Optional[str] = None,
    ):
        self.query = query
        self._headers = headers
        self.export_to = export_to

    @property
    def headers(self):
        return self._headers

    def make_query(self):
        return MySQLConnector().execute(query=self.query)

    def make(self, pprint: Optional[bool] = False, json: Optional[bool] = False):
        return OutputManager(
            data=self.make_query(), headers=self.headers, export_to=self.export_to
        ).run(pprint=pprint, json=json)
