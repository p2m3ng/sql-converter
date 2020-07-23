from pysqldump.adapters.connector import MySQLConnector


def test_mysql_connector_payload():
    connector = MySQLConnector(config='test_config.yaml')
    assert connector.connect.host == "localhost"
    assert connector.connect.db == b"mysql"
    assert connector.connect.user == b"root"
    assert connector.connect.password == b"password"
