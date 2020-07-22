from unittest import mock

import pytest

from sqldumb.query_builder.database import BaseMapper, Database, Table, Field
from sqldumb.converter.connector import MySQLConnector


def test_generate_alias():
    mapper = BaseMapper(name="whatever")
    assert len(mapper._get_alias()) == 3


class TestDatabase:
    @mock.patch.object(Database, "_get_alias")
    def test_database_should_generate_an_alias(self, mock_random):
        mock_random.return_value = "xyz"
        database = Database("myapp_db")
        assert database.name == "myapp_db"
        assert database.alias == "xyz"

    def test_database_should_return_custom_alias(self):
        database = Database(name="myapp_db", alias="xyz")
        assert database.name == "myapp_db"
        assert database.alias == "xyz"


class TestTable:
    @mock.patch.object(Table, "_get_alias")
    def test_table_should_generate_an_alias(self, mock_random):
        mock_random.return_value = "aze"
        table = Table("users")
        assert table.name == "users"
        assert table.alias == "aze"

    def test_table_should_return_custom_alias(self):
        table = Table(name="users", alias="aze")
        assert table.name == "users"
        assert table.alias == "aze"

    @mock.patch.object(MySQLConnector, "execute")
    def test_table_without_fields_should_return_none(self, mocked_connector):
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
        table = Table("users", alias="us")
        assert table.fields == "`us`.`id`, `us`.`user`"


class TestField:
    def test_field_should_not_generate_an_alias(self):
        field = Field("user_id")
        assert field.name == "user_id"
        with pytest.raises(AttributeError):
            field.alias

    def test_field_should_not_return_custom_alias(self):
        with pytest.raises(TypeError):
            Field(name="users", alias="aze")
