import sqlite3


def create_tables():
    db_connection = sqlite3.connect("database.db")
    cursor = db_connection.cursor()

    query = """CREATE TABLE if NOT EXISTS products
                (
                    title         TEXT    not null,
                    description   TEXT    not null,
                    amount        INTEGER not null,
                    price         integer not null,
                    currency_code TEXT    not null,
                    created_by    integer not null,
                    status        TEXT    not null,
                    link          TEXT    not null,
                    file_id       TEXT
                );"""
    cursor.execute(query)

    query = """CREATE TABLE if NOT EXISTS users
                (
                    user_id    integer not null,
                    role       TEXT    not null,
                    first_name TEXT    not null
                );"""
    cursor.execute(query)

    query = """CREATE TABLE if NOT EXISTS orders
                (
                    external_id   TEXT    not null,
                    order_id      TEXT    not null,
                    title         TEXT    not null,
                    product_link  TEXT    not null,
                    user_id       integer not null,
                    price         integer not null,
                    currency_code TEXT    not null,
                    status        TEXT    not null
                );"""
    cursor.execute(query)

    db_connection.commit()
    cursor.close()
    if db_connection:
        db_connection.close()
