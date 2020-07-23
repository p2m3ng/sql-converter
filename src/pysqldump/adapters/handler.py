from .connectors import MySQLConnector, SQLiteConnector
from src.pysqldump.settings.base import get_config


class ConnectorHandler:
    connectors = {"mysql": MySQLConnector, "sqlite": SQLiteConnector}

    def __init__(self, config):
        self.config = config

    def get(self):
        config = get_config(file=self.config)
        connector = self.connectors.get(config.get["db"]["db"])
        return connector(config=self.config)
