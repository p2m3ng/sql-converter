from sql_converter.query_builder.database import Table
from sql_converter.query import Query


def test_headers_should_be_a_list():
    table1 = Table(name="users", fields=["id", "name", "city_id"], alias="us")
    query = Query().add(table1)
    assert query.headers == ["id", "name", "city_id"]


def test_query_as_str():
    table1 = Table(name="users", fields=["id", "name", "city_id"], alias="us")
    query = Query().add(table1)
    expected = """SELECT `us`.`id`, `us`.`name`, `us`.`city_id` 
FROM `users` AS `us` ;"""
    assert str(query) == expected


def test_raw_query():
    table1 = Table(name="users", fields=["id", "name", "city_id"], alias="us")
    table2 = Table(name="city", fields=["id", "name", "country"], alias="cit")
    table3 = Table(name="account", fields=["user_id", "bank"], alias="acc")

    query = (
        Query(prettify=False)
        .add(table1)
        .add(table2)
        .add(table3)
        .join(table1, "id", table2, "id")
        .join(table1, "id", table3, "user_id")
        .where(table2, "country", '= "France"')
        .order_by(table1, "-id")
        .limit(100)
        .build()
    )

    expected = (
        """SELECT `us`.`id`, `us`.`name`, `us`.`city_id`, `cit`.`id`, `cit`.`name`, `cit`.`country`, """
        """`acc`.`user_id`, `acc`.`bank` 
FROM `users` AS `us` 
    INNER JOIN `city` AS `cit` 
        ON `cit`.`id` = `us`.`id` 
    INNER JOIN `account` AS `acc` 
        ON `acc`.`user_id` = `us`.`id` 
WHERE `cit`.`country` = "France" 
ORDER BY `us`.`id` DESC 
LIMIT 100;"""
    )
    assert query == expected


def test_prettified_query():
    table1 = Table(name="users", fields=["id", "name", "city_id"], alias="us")
    table2 = Table(name="city", fields=["id", "name", "country"], alias="cit")
    table3 = Table(name="account", fields=["user_id", "bank"], alias="acc")

    query = (
        Query(prettify=True)
        .add(table1)
        .add(table2)
        .add(table3)
        .join(table1, "id", table2, "id")
        .join(table1, "id", table3, "user_id")
        .where(table2, "country", '= "France"')
        .order_by(table1, "-id")
        .limit(100)
        .build()
    )

    expected = """SELECT us.id, us.name, us.city_id, cit.id, cit.name, cit.country, acc.user_id, acc.bank 
FROM users AS us 
    INNER JOIN city AS cit 
        ON cit.id = us.id 
    INNER JOIN account AS acc 
        ON acc.user_id = us.id 
WHERE cit.country = "France" 
ORDER BY us.id DESC 
LIMIT 100;"""
    assert query == expected
