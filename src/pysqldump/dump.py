from typing import List, Optional

from pysqldump.adapters.connectors import MySQLConnector
from pysqldump.adapters.handler import ConnectorHandler
from pysqldump.domain.manager import OutputManager


class SQLDump:
    def __init__(
        self,
        query: str,
        headers: List[str] = None,
        export_to: Optional[str] = None,
        config: str = "config.yaml",
    ):
        self.query = query
        self._headers = headers
        self.export_to = export_to
        self.config = config

    @property
    def headers(self):
        return self._headers

    def make_query(self):
        connector = ConnectorHandler(config=self.config).get()
        return connector.execute(query=self.query)

    def make(self, pprint: Optional[bool] = False, json: Optional[bool] = False):
        return OutputManager(
            data=self.make_query(), headers=self.headers, export_to=self.export_to
        ).run(pprint=pprint, json=json)
