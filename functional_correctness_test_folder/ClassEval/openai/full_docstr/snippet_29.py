
import sqlite3
from typing import List, Dict, Optional, Tuple


class DatabaseProcessor:
    """
    This is a class for processing a database, supporting to create tables, insert data into the database,
    search for data based on name, and delete data from the database.
    """

    def __init__(self, database_name: str):
        """
        Initialize database name of database processor
        """
        self.database_name = database_name

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_name)

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        """
        Create a new table in the database if it doesn't exist.
        And make id (INTEGER) as PRIMARY KEY, make key1 as TEXT, key2 as INTEGER
        :param table_name: str, the name of the table to create.
        :param key1: str, the name of the first column in the table.
        :param key2: str, the name of the second column in the table.
        >>> db = DatabaseProcessor(':memory:')
        >>> db.create_table('user', 'name', 'age')
        """
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            {key1} TEXT,
            {key2} INTEGER
        )
        """
        with self._get_connection() as conn:
            conn.execute(sql)
            conn.commit()

    def insert_into_database(self, table_name: str, data: List[Dict[str, object]]) -> None:
        """
        Insert data into the specified table in the database.
        :param table_name: str, the name of the table to insert data into.
        :param data: list, a list of dictionaries where each dictionary represents a row of data.
        >>> db = DatabaseProcessor(':memory:')
        >>> db.create_table('user', 'name', 'age')
        >>> db.insert_into_database('user', [
                {'name': 'John', 'age': 25},
                {'name': 'Alice', 'age': 30}
            ])
        """
        if not data:
            return
        keys = data[0].keys()
        placeholders = ", ".join("?" for _ in keys)
        columns = ", ".join(keys)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = [tuple(row[k] for k in keys) for row in data]
        with self._get_connection() as conn:
            conn.executemany(sql, values)
            conn.commit()

    def search_database(self, table_name: str, name: str) -> Optional[List[Tuple]]:
        """
        Search the specified table in the database for rows with a matching name.
        :param table_name: str, the name of the table to search.
        :param name: str, the name to search for.
        :return: list, a list of tuples representing the rows with matching name, if any;
                    otherwise, returns None.
        >>> db = DatabaseProcessor(':memory:')
        >>> db.create_table('user', 'name', 'age')
        >>> db.insert_into_database('user', [{'name': 'John', 'age': 25}])
        >>> db.search_database('user', 'John')
        [(1, 'John', 25)]
        """
        sql = f"SELECT * FROM {table_name} WHERE name = ?"
        with self._get_connection() as conn:
            cur = conn.execute(sql, (name,))
            rows = cur.fetchall()
            return rows if rows else None

    def delete_from_database(self, table_name: str, name: str) -> None:
        """
        Delete rows from the specified table in the database with a matching name.
        :param table_name: str, the name of the table to delete rows from.
        :param name: str, the name to match for deletion.
        >>> db = DatabaseProcessor(':memory:')
        >>> db.create_table('user', 'name', 'age')
        >>> db.insert_into_database('user', [{'name': 'John', 'age': 25}])
        >>> db.delete_from_database('user', 'John')
        >>> db.search_database('user', 'John')
        None
        """
        sql = f"DELETE FROM {table_name} WHERE name = ?"
        with self._get_connection() as conn:
            conn.execute(sql, (name,))
            conn.commit()
