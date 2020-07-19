import pymysql

from sql_converter.settings.settings import get_config

config = get_config()


class MySQLConnector:
    host = config.get["db"]["host"]
    user = config.get["db"]["user"]
    password = config.get["db"]["password"]
    name = config.get["db"]["name"]
    port = config.get["db"]["port"]

    @property
    def connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.name,
            port=self.port,
        )

    def execute(self, query):
        try:
            with self.connect.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.connect.close()
