import sqlite3
from sqlite3 import Error

from iptv.config.logger import logger


def create_connection(db_file):
    """ Create a connection to the database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.info(f"Create a connection to the database")
    except Error as e:
        logger.error(f"Error while connecting to the database: {e}")
    return conn


def close_connection(conn):
    """ Close the connection to the database """
    if conn:
        conn.close()
        logger.info(f"Closed the connection to the database")
