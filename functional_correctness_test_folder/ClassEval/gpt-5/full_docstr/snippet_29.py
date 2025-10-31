import sqlite3
from typing import List, Dict, Optional, Tuple


class DatabaseProcessor:
    """
    This is a class for processing a database, supporting to create tables, insert data into the database, search for data based on name, and delete data from the database.
    """

    def __init__(self, database_name):
        """
        Initialize database name of database processor
        """
        self.database_name = database_name

    def _connect(self):
        return sqlite3.connect(self.database_name)

    def create_table(self, table_name, key1, key2):
        """
        Create a new table in the database if it doesn't exist.
        And make id (INTEGER) as PRIMARY KEY, make key1 as TEXT, key2 as INTEGER
        :param table_name: str, the name of the table to create.
        :param key1: str, the name of the first column in the table.
        :param key2: str, the name of the second column in the table.
        >>> db.create_table('user', 'name', 'age')
        """
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self._quote_ident(table_name)} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {self._quote_ident(key1)} TEXT,
            {self._quote_ident(key2)} INTEGER
        )
        """
        with self._connect() as conn:
            conn.execute(sql)
            conn.commit()

    def insert_into_database(self, table_name, data: List[Dict]):
        """
        Insert data into the specified table in the database.
        :param table_name: str, the name of the table to insert data into.
        :param data: list, a list of dictionaries where each dictionary represents a row of data.
        >>> db.insert_into_database('user', [
                {'name': 'John', 'age': 25},
                {'name': 'Alice', 'age': 30}
            ])
        """
        if not data:
            return

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"PRAGMA table_info({self._quote_ident(table_name)})")
            cols_info = cursor.fetchall()
            table_cols = {row[1] for row in cols_info}  # column names
            # Exclude 'id' if present; it's auto-increment
            if 'id' in table_cols:
                table_cols.remove('id')

            # Determine insertion columns from first item, filtered by table columns
            insert_cols = [col for col in data[0].keys() if col in table_cols]
            if not insert_cols:
                return

            placeholders = ", ".join(["?"] * len(insert_cols))
            col_list = ", ".join(self._quote_ident(c) for c in insert_cols)
            sql = f"INSERT INTO {self._quote_ident(table_name)} ({col_list}) VALUES ({placeholders})"

            rows = []
            for item in data:
                row = tuple(item.get(col) for col in insert_cols)
                rows.append(row)

            cursor.executemany(sql, rows)
            conn.commit()

    def search_database(self, table_name, name) -> Optional[List[Tuple]]:
        """
        Search the specified table in the database for rows with a matching name.
        :param table_name: str, the name of the table to search.
        :param name: str, the name to search for.
        :return: list, a list of tuples representing the rows with matching name, if any;
                    otherwise, returns None.
        >>> db.search_database('user', 'John')
        [(1, 'John', 25)]
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            # Assume the table has a 'name' column as per usage examples
            sql = f"SELECT * FROM {self._quote_ident(table_name)} WHERE {self._quote_ident('name')} = ?"
            cursor.execute(sql, (name,))
            rows = cursor.fetchall()
            return rows if rows else None

    def delete_from_database(self, table_name, name):
        """
        Delete rows from the specified table in the database with a matching name.
        :param table_name: str, the name of the table to delete rows from.
        :param name: str, the name to match for deletion.
        >>> db.delete_from_database('user', 'John')
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            sql = f"DELETE FROM {self._quote_ident(table_name)} WHERE {self._quote_ident('name')} = ?"
            cursor.execute(sql, (name,))
            conn.commit()

    @staticmethod
    def _quote_ident(identifier: str) -> str:
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be a string")
        if '"' in identifier:
            identifier = identifier.replace('"', '""')
        return f'"{identifier}"'
