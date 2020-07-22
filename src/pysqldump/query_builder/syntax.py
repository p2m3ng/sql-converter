from pysqldump.query_builder.database import Table
from typing import Optional
from abc import ABC, abstractmethod


class SQLExpression(ABC):
    @abstractmethod
    def build(self) -> str:
        """"""


class Select(SQLExpression):
    def __init__(self):
        self.tables: list = []

    @property
    def fields(self) -> (str, None):
        if len(self.tables) > 1:
            return ", ".join([table.fields for table in self.tables])
        elif len(self.tables) == 1:
            return self.tables[0].fields

    def build(self) -> str:
        return f"SELECT {self.fields} "

    def add(self, table) -> "Select":
        self.tables.append(table)
        return self

    def __repr__(self) -> str:
        return f'<Select: {", ".join([str(table.name) for table in self.tables])}>'

    def __str__(self) -> str:
        return self.build()


class From(SQLExpression):
    def __init__(self, table: Table):
        self.table: Table = table

    def build(self) -> str:
        if self.table.database.name:
            database = f"`{self.table.database.name}`."
        else:
            database = ""
        return f"\nFROM {database}`{self.table.name}` AS `{self.table.alias}` "

    def __repr__(self) -> str:
        return f"<From # {self.table.name} ({self.table.alias})>"

    def __str__(self) -> str:
        return self.build()


class Join(SQLExpression):
    def __init__(
        self,
        table1: Table,
        field1: str,
        table2: Table,
        field2: str,
        type: Optional[str] = None,
    ):
        self.table1 = table1
        self.field1 = field1
        self.table2 = table2
        self.field2 = field2
        self.type = type

    def build(self) -> str:
        return (
            f"\n{(' '*4)}{self.get_join_type()} JOIN `{self.table2.name}` AS `{self.table2.alias}` "
            f"\n{(' '*8)}ON `{self.table2.alias}`.`{self.field2}` = `{self.table1.alias}`.`{self.field1}` "
        )

    def get_join_type(self):
        if not self.type:
            return "INNER"
        return self.type.upper().replace(" JOIN", "")

    def __repr__(self) -> str:
        return f"<Join: {self.table1.name} and {self.table2.name}>"

    def __str__(self) -> str:
        return self.build()


class Where(SQLExpression):
    def __init__(self, table: Table, field: str, predicate: str = ""):
        self.table = table
        self.field = field
        self.predicate = predicate

    def build(self) -> str:
        return f"\nWHERE `{self.table.alias}`.`{self.field}` {self.predicate} "

    def __repr__(self):
        return f"<Where: {self.table.name} :: {self.field} :: {self.predicate}>"

    def __str__(self):
        return self.build()


class OrderBy(SQLExpression):
    def __init__(self, table: Table, field: str):
        self.table = table
        self.field = field

    def build(self) -> str:
        if self.field is None:
            raise AttributeError("'field' attribute cannot be set to 'None'.")
        elif self.field.startswith("-"):
            return f"\nORDER BY `{self.table.alias}`.`{self.field[1:]}` DESC "
        elif not self.field.startswith("-"):
            return f"\nORDER BY `{self.table.alias}`.`{self.field}` ASC "

    def __repr__(self):
        return f"<OrderBy # {self.table.name} : {self.field}>"

    def __str__(self):
        return self.build()


class Limit(SQLExpression):
    def __init__(self, number: int):
        self.number = number

    def build(self) -> str:
        return f"\nLIMIT {self.number}"

    def __repr__(self):
        return f"<Limit: {self.number}>"

    def __str__(self):
        return self.build()
