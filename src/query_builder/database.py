import random
import string
from src.converter.connector import MySQLConnector
from src.converter.formatters import DictFormatter, JsonFormatter


class BaseMapper:
    connector = MySQLConnector()

    def __init__(self, name, alias=None):
        self.name = name
        self._alias = alias

    @property
    def alias(self):
        if self._alias is None:
            self.alias = self._get_alias()
        return self._alias

    @alias.setter
    def alias(self, value):
        self._alias = value

    @staticmethod
    def _get_alias():
        return "".join([random.choice(string.ascii_letters) for _ in range(3)])


class Database(BaseMapper):
    def show_databases(self):
        databases = self.connector.execute(query="SHOW DATABASES;")
        return [database[0] for database in databases]

    def show_tables(self):
        self.connector.name = self.name
        tables = self.connector.execute(query="SHOW TABLES;")
        return [table[0] for table in tables]


class Table(BaseMapper):
    def __init__(self, name, alias=None, fields=None, database=""):
        super(Table, self).__init__(name=name, alias=alias)
        self.database = Database(name=database)
        self._fields = fields

    def describe(self, json=False):
        data = self.connector.execute(query=f"DESCRIBE {self.name}")
        headers = ["field", "type", "null", "key", "default", "extra"]
        if json:
            return JsonFormatter(headers=headers, data=data, export_to=None).use()
        return DictFormatter(headers=headers, data=data, export_to=None).to_dict()

    def get_headers(self):
        return [header["field"] for header in self.describe()]

    @property
    def fields(self):
        if self._fields is None:
            self._fields = self.get_headers()
        return ", ".join([f"`{self.alias}`.`{field}`" for field in self._fields])


class Field(BaseMapper):
    def __init__(self, name):
        super(Field, self).__init__(name=name)

    @property
    def alias(self):
        raise AttributeError("'Field' object has no attribute 'alias'")
