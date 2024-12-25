import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Create a connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(f"Error while connecting to the database: {e}")
    return conn


def close_connection(conn):
    """ Close the connection to the database """
    if conn:
        conn.close()
