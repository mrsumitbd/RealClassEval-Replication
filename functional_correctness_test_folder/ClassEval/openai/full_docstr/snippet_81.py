
class SQLQueryBuilder:
    """
    This class provides to build SQL queries, including SELECT, INSERT, UPDATE, and DELETE statements. 
    """

    @staticmethod
    def _quote(value):
        """Return the value quoted as a string."""
        return f"'{value}'"

    @staticmethod
    def _build_where(where):
        """Build the WHERE clause from a dictionary."""
        if not where:
            return ""
        conditions = [
            f"{k}={SQLQueryBuilder._quote(v)}" for k, v in where.items()]
        return " WHERE " + " AND ".join(conditions)

    @staticmethod
    def select(table, columns='*', where=None):
        """
        Generate the SELECT SQL statement from the given parameters.
        :param table: str, the query table in database.
        :param columns: list of str, ['col1', 'col2'].
        :param where: dict, {key1: value1, key2: value2 ...}. The query condition.
        return query: str, the SQL query statement.
        >>> SQLQueryBuilder.select('table1', columns = ["col1","col2"], where = {"age": 15})
        "SELECT col1, col2 FROM table1 WHERE age='15'"
        """
        if isinstance(columns, list):
            cols = ", ".join(columns)
        else:
            cols = columns
        query = f"SELECT {cols} FROM {table}"
        query += SQLQueryBuilder._build_where(where)
        return query

    @staticmethod
    def insert(table, data):
        """
        Generate the INSERT SQL statement from the given parameters.
        :param table: str, the table to be inserted in database.
        :param data: dict, the key and value in SQL insert statement
        :return query: str, the SQL insert statement.
        >>> SQLQueryBuilder.insert('table1', {'name': 'Test', 'age': 14})
        "INSERT INTO table1 (name, age) VALUES ('Test', '14')"
        """
        cols = ", ".join(data.keys())
        vals = ", ".join(SQLQueryBuilder._quote(v) for v in data.values())
        return f"INSERT INTO {table} ({cols}) VALUES ({vals})"

    @staticmethod
    def delete(table, where=None):
        """
        Generate the DELETE SQL statement from the given parameters.
        :param table: str, the table that will be excuted with DELETE operation in database
        :param where: dict, {key1: value1, key2: value2 ...}. The query condition.
        :return query: str, the SQL delete statement.
        >>> SQLQueryBuilder.delete('table1', {'name': 'Test', 'age': 14})
        "DELETE FROM table1 WHERE name='Test' AND age='14'"
        """
        query = f"DELETE FROM {table}"
        query += SQLQueryBuilder._build_where(where)
        return query

    @staticmethod
    def update(table, data, where=None):
        """
        Generate the UPDATE SQL statement from the given parameters.
        :param table: str, the table that will be excuted with UPDATE operation in database
        :param data: dict, the key and value in SQL update statement
        :param where: dict, {key1: value1, key2: value2 ...}. The query condition.
        >>> SQLQueryBuilder.update('table1', {'name': 'Test2', 'age': 15}, where = {'name':'Test'})
        "UPDATE table1 SET name='Test2', age='15' WHERE name='Test'"
        """
        set_clause = ", ".join(
            f"{k}={SQLQueryBuilder._quote(v)}" for k, v in data.items())
        query = f"UPDATE {table} SET {set_clause}"
        query += SQLQueryBuilder._build_where(where)
        return query
