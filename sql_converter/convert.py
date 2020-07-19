from typing import List, Optional

from sql_converter.converter.connector import MySQLConnector
from sql_converter.converter.manager import OutputManager
from sql_converter.query import Query


class SQLConvert:
    def __init__(
        self, query: (Query, str), headers: List[str], export_to: Optional[str] = None,
    ):
        self.query = query
        self._headers = headers
        self.export_to = export_to

    @property
    def headers(self):
        if self._headers is None:
            raise AttributeError("`headers` attribute should contain data.")
        return self._headers

    def make_query(self):
        return MySQLConnector().execute(query=self.query)

    def make(self, pprint: Optional[bool] = False, json: Optional[bool] = False):
        return OutputManager(
            data=self.make_query(), headers=self.headers, export_to=self.export_to
        ).run(pprint=pprint, json=json)
