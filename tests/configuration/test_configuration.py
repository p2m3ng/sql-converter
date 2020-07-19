import os
from unittest import mock

import pytest

from settings.base import get_config, CONFIG_FILES_PATH
from click.testing import CliRunner
from src.cli import cli


@pytest.fixture()
def config():
    return get_config("config.sample.yaml")


fake_env = {
    "SQL_EXPORT_DB_HOST": "test_localhost",
    "SQL_EXPORT_DB_PORT": "1234",
    "SQL_EXPORT_DB_USER": "root",
    "SQL_EXPORT_DB_NAME": "mysql database name",
    "SQL_EXPORT_DB_PASSWORD": "psswd",
}


def test_file_absolute_path(config):
    path = config.get_file_path()
    assert "settings/files/config.sample.yaml" in path


def test_cli_config_should_dump_config_file():
    testing_file = os.path.join(CONFIG_FILES_PATH, "test.yaml")

    runner = CliRunner()
    result = runner.invoke(
        cli, ["config", "-n", "mysqldbname", "-p", "psswd", "-f", "test.yaml"]
    )
    assert result.exit_code == 0
    assert result.output == "New config file generated.\n"
    assert os.path.exists(testing_file)

    os.remove(testing_file)


def test_cli_config_default_values():
    testing_file = os.path.join(CONFIG_FILES_PATH, "test.yaml")

    runner = CliRunner()
    runner.invoke(
        cli, ["config", "-n", "mysqldbname", "-p", "psswd", "-f", "test.yaml"]
    )
    config = get_config("test.yaml")
    expected = {
        "db": {
            "host": "localhost",
            "name": "mysqldbname",
            "password": "psswd",
            "port": 3306,
            "user": "root",
        }
    }
    assert config.get_file_content() == expected

    os.remove(testing_file)


def test_should_get_content_from_file(config):
    content = config.get_file_content()
    with pytest.raises(KeyError):
        os.environ["SQL_EXPORT_DB_HOST"]
    expected = {
        "db": {
            "host": "localhost",
            "port": 0,
            "user": "root",
            "name": "mysql database name",
            "password": "psswd",
        }
    }
    assert content == expected


@mock.patch.dict(os.environ, fake_env)
def test_should_get_content_from_environment_variables():
    config = get_config("config-test.yaml")
    assert config.get["db"]["host"] == "test_localhost"
    assert os.environ["SQL_EXPORT_DB_HOST"]
    os.remove(config.get_file_path())


@mock.patch.dict(os.environ, fake_env)
def test_db_port_should_be_integer():
    config = get_config("config-test.yaml")
    assert isinstance(config.get["db"]["port"], int)


def test_get_item(config):
    id = config.get["db"]["host"]
    assert id == "localhost"


def test_get_wrong_item(config):
    with pytest.raises(KeyError):
        config.get["whatever"]


def test_file_does_not_exist_shoult_raise_exception():
    with pytest.raises(FileNotFoundError):
        get_config("whatever.yaml").get["whatever"]


def test_should_print_repr_for_config(config):
    assert repr(config) == "<Configuration: config.sample.yaml>"
