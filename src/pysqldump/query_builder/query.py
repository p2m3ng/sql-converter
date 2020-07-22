from pysqldump.query_builder.database import Table
from pysqldump.query_builder.syntax import Select, From, Join, Where, OrderBy, Limit


class QueryBuilder:
    query = ""

    def __init__(self, prettify: bool = False):
        self._select = Select()
        self.tables = []
        self._from = ""
        self._joins = ""
        self._where = ""
        self._order_by = ""
        self._limit = ""
        self.prettify = prettify

    @property
    def headers(self):
        fields = self._select.fields.replace("`", "").split(", ")
        return [field.split(".")[1] for field in fields]

    @property
    def from_(self):
        self._from = From(self.tables[0])
        return self._from

    def add(self, table):
        self.tables.append(table)
        self._select.add(table)
        return self

    def join(
        self, table1: Table, field1: str, table2: Table, field2: str, type: str = ""
    ):
        self._joins += Join(
            table1=table1, field1=field1, table2=table2, field2=field2, type=type
        ).build()
        return self

    def where(self, table: Table, field: str, predicate: str = ""):
        self._where = Where(table=table, field=field, predicate=predicate).build()
        return self

    def order_by(self, table, field):
        self._order_by = OrderBy(table=table, field=field).build()
        return self

    def limit(self, number: int):
        self._limit = Limit(number=number).build()
        return self

    def build(self):
        sql_expression = f"{self._select.build()}{self.from_}{self._joins}{self._where}{self._order_by}{self._limit};"
        if self.prettify:
            return self._prettify(query=sql_expression)
        return sql_expression

    @staticmethod
    def _prettify(query: str):
        return query.replace("`", "")

    def __str__(self):
        return self.build()
