import os
import pytest
from settings.settings import get_config, BASE_DIR, Config
from unittest import mock


@pytest.fixture()
def config():
    return get_config("config.sample.yaml")


fake_env = {
    'SQL_EXPORT_DB_HOST': 'test_localhost',
    'SQL_EXPORT_DB_PORT': "1234",
    'SQL_EXPORT_DB_USER': 'root',
    'SQL_EXPORT_DB_NAME': 'mysql database name',
    'SQL_EXPORT_DB_PASSWORD': 'psswd'
}


def test_file_absolute_path(config):
    path = config.get_file_path()
    assert "settings/files/config.sample.yaml" in path


def test_should_get_content_from_file(config):
    content = config.get_file_content()
    with pytest.raises(KeyError):
        env = os.environ["SQL_EXPORT_DB_HOST"]
    expected = {'db':
        {
            'host': 'localhost',
            'port': 0,
            'user': 'root',
            'name': 'mysql database name',
            'password': 'psswd'
        }
    }
    assert content == expected


@mock.patch.dict(os.environ, fake_env)
def test_should_get_content_from_environment_variables():
    config = get_config("config-test.yaml")
    assert config.get["db"]["host"] == "test_localhost"
    assert os.environ['SQL_EXPORT_DB_HOST']
    os.remove(config.get_file_path())


def test_get_item(config):
    id = config.get["db"]['host']
    assert id == "localhost"


def test_get_wrong_item(config):
    with pytest.raises(KeyError):
        whatever = config.get["whatever"]


def test_should_print_repr_for_config(config):
    assert repr(config) == "<Configuration: config.sample.yaml>"
