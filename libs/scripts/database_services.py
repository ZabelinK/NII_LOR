import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# The connection is opening by default settings.
# There is no need  for now to manage anything except user name and database name
def open_db_connection(database_name, user_name):
    try:
        connection = psycopg2.connect(
                               dbname=database_name,
                               user=user_name,
                               host="127.0.0.1",
                               port="5432")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def close_db_connection(connection):
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")


def execute_query(connection, query):
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def create_database(connection, database_name):
    execute_query(connection, sql.SQL("CREATE DATABASE {} WITH ENCODING 'UTF8'").format(
        sql.Identifier(database_name))
    )
    print("Database " + database_name + " has been created")


def drop_database(connection, database_name):
    execute_query(connection, sql.SQL("DROP DATABASE IF EXISTS {}").format(
        sql.Identifier(database_name))
                  )
    print("Database " + database_name + " has been removed")


def drop_table(connection, table):
    drop_table_query = '''DROP TABLE IF EXISTS {0};'''.format(table)
    cursor = connection.cursor()
    cursor.execute(drop_table_query)
