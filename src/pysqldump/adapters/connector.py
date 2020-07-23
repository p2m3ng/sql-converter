import pymysql

from pysqldump.settings.base import get_config


class MySQLConnector:
    def __init__(self, config: str = 'config.yaml'):
        self.config = get_config(config)
        
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
