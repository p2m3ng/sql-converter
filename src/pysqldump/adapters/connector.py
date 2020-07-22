import pymysql

from pysqldump.settings.base import get_config

config = get_config()


class MySQLConnector:
    @property
    def connect(self):
        return pymysql.connect(
            host=config.get["db"]["host"],
            user=config.get["db"]["user"],
            password=config.get["db"]["password"],
            db=config.get["db"]["name"],
            port=config.get["db"]["port"],
        )

    def execute(self, query: str):
        try:
            with self.connect.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.connect.close()
