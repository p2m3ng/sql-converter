from pysqldump.adapters.connector import MySQLConnector


def test_mysql_connector_payload():
    connector = MySQLConnector(config='test_config.yaml')
    assert connector.connect.host == "localhost"
    assert connector.connect.db == b"classicmodels"
    assert connector.connect.user == b"root"
    assert connector.connect.password == b"password"


def test_mysql_connector_cursor_should_return_dict():
    connector = MySQLConnector(config="test_config.yaml")
    result = connector.execute("SHOW TABLES;")
    assert isinstance(result, list)
    for data in result:
        assert isinstance(data, dict)