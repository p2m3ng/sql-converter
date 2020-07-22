from unittest import mock

import pytest

from pysqldump.adapters.connector import MySQLConnector
from pysqldump.query_builder.database import Table
from pysqldump.query_builder.syntax import Select, From, Join, Where, OrderBy, Limit


class TestSelect:
    def test_should_select_given_fields(self):
        table = Table(
            name="users", fields=["username", "email", "password"], alias="us"
        )
        select = Select().add(table=table)
        assert (
            select.build() == "SELECT `us`.`username`, `us`.`email`, `us`.`password` "
        )

    @mock.patch.object(MySQLConnector, "execute")
    def test_no_filled_field_should_select_everything(self, mocked_connector):
        mocked_connector.return_value = [
            {
                "field": "id",
                "type": "int[10] unsigned",
                "null": "NO",
                "key": "PRI",
                "default": None,
                "extra": "auto_increment",
            },
            {
                "field": "user",
                "type": "varchar[200] unsigned",
                "null": "NO",
                "key": "",
                "default": None,
                "extra": "",
            },
        ]
        table = Table(name="users", alias="us")
        select = Select().add(table=table)
        assert select.build() == "SELECT `us`.`id`, `us`.`user` "

    def test_repr_should_return_selected_tables_names(self):
        table1 = Table("users")
        table2 = Table("books")
        select = Select().add(table=table1).add(table=table2)
        assert repr(select) == "<Select: users, books>"

    def test_str_should_return_sql_select_expression(self):
        table1 = Table(
            name="users", fields=["username", "email", "password"], alias="us"
        )
        select = Select().add(table=table1)
        assert str(select) == "SELECT `us`.`username`, `us`.`email`, `us`.`password` "


class TestFrom:
    def test_should_return_from_expression_with_alias(self):
        table = Table(name="users", alias="us")
        from_expression = From(table=table)
        assert from_expression.build() == "\nFROM `users` AS `us` "

    def test_repr_should_return_tablename_and_alias(self):
        table = Table(name="users", alias="us")
        from_expression = From(table=table)
        assert repr(from_expression) == "<From # users (us)>"

    def test_should_use_database_name(self):
        table = Table(database="sample", name="users", alias="us")
        from_expression = From(table=table)
        assert from_expression.build() == "\nFROM `sample`.`users` AS `us` "


class TestJoin:
    @pytest.fixture
    def table1(self):
        return Table(
            name="users", fields=["id", "username", "email", "password"], alias="us"
        )

    @pytest.fixture
    def table2(self):
        return Table(
            name="address", fields=["id", "user_id", "city", "country"], alias="ad"
        )

    def test_should_return_inner_join_expression(self, table1, table2):
        join = Join(table1=table1, field1="id", table2=table2, field2="user_id")
        expected = """\n    INNER JOIN `address` AS `ad` 
        ON `ad`.`user_id` = `us`.`id` """
        assert join.build() == expected
        assert str(join) == expected

    def test_should_return_left_join_expression(self, table1, table2):
        join = Join(
            table1=table1, field1="id", table2=table2, field2="user_id", type="left"
        )
        expected = """\n    LEFT JOIN `address` AS `ad` 
        ON `ad`.`user_id` = `us`.`id` """
        assert join.build() == expected

    def test_should_return_right_join_expression(self, table1, table2):
        join = Join(
            table1=table1, field1="id", table2=table2, field2="user_id", type="right"
        )
        expected = """\n    RIGHT JOIN `address` AS `ad` 
        ON `ad`.`user_id` = `us`.`id` """
        assert join.build() == expected

    def test_should_return_full_outer_join_expression(self, table1, table2):
        join = Join(
            table1=table1,
            field1="id",
            table2=table2,
            field2="user_id",
            type="full outer join",
        )
        expected = """\n    FULL OUTER JOIN `address` AS `ad` 
        ON `ad`.`user_id` = `us`.`id` """
        assert join.build() == expected

    def test_repr_should_return_both_tables_names(self):
        table1 = Table(
            name="users", fields=["id", "username", "email", "password"], alias="us"
        )
        table2 = Table(
            name="address", fields=["id", "user_id", "city", "country"], alias="ad"
        )
        join = Join(table1=table1, field1="id", table2=table2, field2="user_id")
        assert repr(join) == "<Join: users and address>"


class TestWhere:
    def test_should_return_where_expression(self):
        table = Table(
            name="users", fields=["id", "username", "email", "password"], alias="us"
        )
        where = Where(table=table, field="id", predicate="= 12")
        assert where.build() == "\nWHERE `us`.`id` = 12 "

    def test_repr_should_return_where_expression_details(self):
        table = Table(
            name="users", fields=["id", "username", "email", "password"], alias="us"
        )
        where = Where(table=table, field="id", predicate="= 12")
        assert repr(where) == "<Where: users :: id :: = 12>"

    def test_str_should_return_where_expression(self):
        table = Table(
            name="users", fields=["id", "username", "email", "password"], alias="us"
        )
        where = Where(table=table, field="id", predicate="= 12")
        assert str(where) == "\nWHERE `us`.`id` = 12 "


class TestOrderBy:
    @pytest.fixture
    def table(self):
        return Table(
            name="users", fields=["id", "username", "email", "password"], alias="us"
        )

    def test_should_return_ascendant_order(self, table):
        order_by = OrderBy(table=table, field="id")
        assert order_by.build() == "\nORDER BY `us`.`id` ASC "

    def test_should_return_descendant_order(self, table):
        order_by = OrderBy(table=table, field="-id")
        assert order_by.build() == "\nORDER BY `us`.`id` DESC "

    def test_none_fields_returns_void_string(self):
        table = Table(name="users", fields="id", alias="us")
        order_by = OrderBy(table=table, field=None)
        with pytest.raises(AttributeError):
            order_by.build()

    def test_should_return_order_by_tablename_and_field(self, table):
        order_by = OrderBy(table=table, field="-id")
        assert repr(order_by) == "<OrderBy # users : -id>"

    def test_str_should_return_order_by_expression(self, table):
        order_by = OrderBy(table=table, field="id")
        assert str(order_by) == "\nORDER BY `us`.`id` ASC "


class TestLimit:
    def test_limit_should_return_length_limit_expression(self):
        limit = Limit(number=100)
        assert limit.build() == "\nLIMIT 100"

    def test_repr_limit_should_return_details(self):
        limit = Limit(number=100)
        assert repr(limit) == "<Limit: 100>"

    def test_str_limit_should_return_length_limit_expression(self):
        limit = Limit(number=100)
        assert str(limit) == "\nLIMIT 100"
