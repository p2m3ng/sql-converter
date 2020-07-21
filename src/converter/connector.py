import pymysql

from settings.base import get_config

config = get_config()


class MySQLConnector:
    def __init__(self):
        self._cursor = ""

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value

    @property
    def connect(self):
        return pymysql.connect(
            host=config.get["db"]["host"],
            user=config.get["db"]["user"],
            password=config.get["db"]["password"],
            db=config.get["db"]["name"],
            port=config.get["db"]["port"],
        )

    def execute(self, query):
        try:
            with self.connect.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.connect.close()
