import sqlite3
from sqlite3 import Error
import os


class DatabaseManager:
    def __init__(self, db_file):
        """Initialize the database connection."""
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish the connection to the SQLite database and create tables if they don't exist."""
        try:
            # Verificar si la carpeta existe, y crearla si no
            directory = os.path.dirname(self.db_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Establecer la conexión a la base de datos SQLite
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            print(f"Connection established to the database {self.db_file}")

            # Verificar si las tablas necesarias existen y, si no, crearlas
            self.check_and_create_tables()

        except Error as e:
            print(f"Error connecting to the database: {e}")

    def check_and_create_tables(self):
        """Check if required tables exist, and create them if they don't."""
        try:
            # Obtener el listado de las tablas existentes
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            existing_tables = [table[0] for table in self.cursor.fetchall()]

            # Verificar si la tabla 'channels' existe
            if 'channels' not in existing_tables:
                self.create_channels_table()

            # Aquí puedes agregar más tablas si es necesario, por ejemplo:
            # if 'another_table' not in existing_tables:
            #     self.create_another_table()

        except Error as e:
            print(f"Error checking tables: {e}")

    def create_channels_table(self):
        """Create the 'channels' table if it doesn't exist."""
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL
            )
            """)
            print("Table 'channels' created or already exists.")
            self.connection.commit()
        except Error as e:
            print(f"Error creating the channels table: {e}")

    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL
            )
            """)
            print("Table 'channels' created or already exists.")
            self.connection.commit()
        except Error as e:
            print(f"Error creating the tables: {e}")

    def execute_query(self, query, params=None):
        """Execute an SQL query (INSERT, UPDATE, DELETE, etc.)."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"Error executing the query: {e}")

    def fetch_all(self, query, params=None):
        """Fetch all results from a SELECT query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching the data: {e}")
            return []

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Connection closed.")
        else:
            print("No open connection.")

    def __enter__(self):
        """This is called when entering the 'with' block."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """This is called when exiting the 'with' block."""
        pass
        # self.close()
