from src.pysqldump.adapters.handler import ConnectorHandler


def test_connector_factory_should_return_sqlite():
    factory = ConnectorHandler(config="test_sqlite_config.yaml")
    connector = factory.get()
    assert repr(connector) == "<SQLiteConnector: test_sqlite_config.yaml>"


def test_connector_factory_should_return_mysql():
    factory = ConnectorHandler(config="test_config.yaml")
    connector = factory.get()
    assert repr(connector) == "<MySQLConnector: test_config.yaml>"
