import pymysql
import sqlite3
import abc
from pysqldump.settings.base import get_config


class AbstractConnector(abc.ABC):  # pragma: no cover
    def __init__(self, config: str = "config.yaml"):
        self.config = get_config(config)

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def execute(self, query: str):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.config.file}>"


class MySQLConnector(AbstractConnector):
    @property
    def connect(self):
        return pymysql.connect(
            host=self.config.get["db"]["host"],
            user=self.config.get["db"]["user"],
            password=self.config.get["db"]["password"],
            db=self.config.get["db"]["name"],
            port=self.config.get["db"]["port"],
        )

    def execute(self, query: str):
        try:
            with self.connect.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.connect.close()


class SQLiteConnector(AbstractConnector):
    @property
    def connect(self):
        return sqlite3.connect(database=self.config.get["db"]["name"])

    def execute(self, query):
        try:
            with self.connect as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query)
                return [dict(row) for row in cursor.fetchall()]
        finally:
            self.connect.close()
