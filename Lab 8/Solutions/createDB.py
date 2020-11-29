import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"sqlite.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        login text PRIMARY KEY,
                                        password text NOT NULL
                                    ); """

    sql_create_mess_table = """CREATE TABLE IF NOT EXISTS messages (
                                    id integer PRIMARY KEY,
                                    fromUser text NOT NULL,
                                    toUser text NOT NULL,
                                    date text NOT NULL,
                                    time text NOT NULL
                                );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_users_table)

        create_table(conn, sql_create_mess_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()