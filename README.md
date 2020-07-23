# PySqlDump

[![pipeline status](https://gitlab.com/p2m3ng/sql-converter/badges/master/pipeline.svg)](https://gitlab.com/p2m3ng/sql-converter/-/commits/master)
[![coverage report](https://gitlab.com/p2m3ng/sql-converter/badges/master/coverage.svg)](https://gitlab.com/p2m3ng/sql-converter/-/commits/master)

Dump SQL queries result in chosen format.

## Presentation

This tool can be used by developers to dump SQL data to various data structures
and export it to JSON or CSV files. 
Dropping database tables or query results becomes easy. 

## Installation

Clone repository: 

    $ git@gitlab.com:p2m3ng/sql-converter.git

Or install with pip:

    $ pip install git+ssh://git@gitlab.com/p2m3ng/sql-converter

Create a virtual environment: 

    $ python3 -m venv venv
    $ source venv/bin/activate
    
Install: 

    $ make install

### Configuration

For database configuration, see: 

    $ pysqldump config --help
    
For quick config: 

    $ pysqldump config -d mysql -n Chinook -p password
    
It will create a config file in `src/pysqldump/settings/config.yaml`
    
### Tests

Download mysql databases from this 
[repository](https://github.com/lerocha/chinook-database) and launch mysql 
docker on `./volume/mysql`. The process may take some time. 

    $ make test-env
    $ make test

To check coverage:

    $ make coverage

## Usage:

### Json

```python
from pysqldump.dump import SQLDump

export = SQLDump(
    query="SELECT EmployeeId, LastName, FirstName, Title FROM Employee LIMIT 1",
    export_to="employees.json",
    config="test_sqlite_config.yaml"
)
export.make(pprint=True, json=False)
```

Output: 

```
[
  {
    "EmployeeId": 1,
    "LastName": "Adams",
    "FirstName": "Andrew",
    "Title": "General Manager"
  }
]
```

### CSV

```python
from pysqldump.dump import SQLDump

export = SQLDump(
    query="SELECT EmployeeId, LastName, FirstName, Title FROM Employee LIMIT 1",
    export_to="employees.csv"
)
export.make(pprint=True, json=False)
```

Output: 

```
EmployeeId|LastName|FirstName|Title
1|Adams|Andrew|General Manager
```

### Console

```python
export = SQLDump(
    query="SELECT EmployeeId, LastName, FirstName, Title FROM Employee LIMIT 1",
    config="test_sqlite_config.yaml"
)
```

```python
# Returns a json string
data = export.make(pprint=True, json=True)

# Returns None
data = export.make(pprint=True)

# Returns a dict
data = export.make()
```

### Parameters: 

- `query` (required) is a raw SQL query 
- `export_to` gets file format by its extension (`*.csv` or `*.json`) or 
returns data as a list of dictionaries if `None`. Default: `None`
- `config` uses the dedicated config file. Default: `config.yaml`
- `pprint` prints chosen output to console. Default: `False`
- `json` presents output as usable JSON string. Default: `False`

## Addendum

According to the dedicated config file parameters, you can use several 
connectors at runtime: 

```python
from pysqldump.adapters.handler import ConnectorHandler

connector = ConnectorHandler(config='test_sqlite_config.yaml').get()
data = connector.execute(query="SELECT * FROM Employee")
```

The `execute(query=query)` returns a dict. 