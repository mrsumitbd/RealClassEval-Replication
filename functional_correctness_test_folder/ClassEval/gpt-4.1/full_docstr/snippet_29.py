
import sqlite3


class DatabaseProcessor:
    """
    This is a class for processing a database, supporting to create tables, insert data into the database, search for data based on name, and delete data from the database.
    """

    def __init__(self, database_name):
        """
        Initialize database name of database processor
        """
        self.database_name = database_name

    def create_table(self, table_name, key1, key2):
        """
        Create a new table in the database if it doesn't exist.
        And make id (INTEGER) as PRIMARY KEY, make key1 as TEXT, key2 as INTEGER
        :param table_name: str, the name of the table to create.
        :param key1: str, the name of the first column in the table.
        :param key2: str, the name of the second column in the table.
        >>> db.create_table('user', 'name', 'age')
        """
        conn = sqlite3.connect(self.database_name)
        c = conn.cursor()
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {key1} TEXT,
            {key2} INTEGER
        )
        """
        c.execute(sql)
        conn.commit()
        conn.close()

    def insert_into_database(self, table_name, data):
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
        keys = list(data[0].keys())
        placeholders = ','.join(['?'] * len(keys))
        columns = ','.join(keys)
        values = [tuple(d[k] for k in keys) for d in data]
        conn = sqlite3.connect(self.database_name)
        c = conn.cursor()
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        c.executemany(sql, values)
        conn.commit()
        conn.close()

    def search_database(self, table_name, name):
        """
        Search the specified table in the database for rows with a matching name.
        :param table_name: str, the name of the table to search.
        :param name: str, the name to search for.
        :return: list, a list of tuples representing the rows with matching name, if any;
                    otherwise, returns None.
        >>> db.search_database('user', 'John')
        [(1, 'John', 25)]
        """
        conn = sqlite3.connect(self.database_name)
        c = conn.cursor()
        # Find the name column
        c.execute(f"PRAGMA table_info({table_name})")
        columns = c.fetchall()
        name_col = None
        for col in columns:
            if col[2] == "TEXT":
                name_col = col[1]
                break
        if not name_col:
            conn.close()
            return None
        c.execute(f"SELECT * FROM {table_name} WHERE {name_col}=?", (name,))
        rows = c.fetchall()
        conn.close()
        if rows:
            return rows
        else:
            return None

    def delete_from_database(self, table_name, name):
        """
        Delete rows from the specified table in the database with a matching name.
        :param table_name: str, the name of the table to delete rows from.
        :param name: str, the name to match for deletion.
        >>> db.delete_from_database('user', 'John')
        """
        conn = sqlite3.connect(self.database_name)
        c = conn.cursor()
        # Find the name column
        c.execute(f"PRAGMA table_info({table_name})")
        columns = c.fetchall()
        name_col = None
        for col in columns:
            if col[2] == "TEXT":
                name_col = col[1]
                break
        if not name_col:
            conn.close()
            return
        c.execute(f"DELETE FROM {table_name} WHERE {name_col}=?", (name,))
        conn.commit()
        conn.close()
