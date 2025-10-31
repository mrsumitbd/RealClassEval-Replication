
class SQLQueryBuilder:
    """
    This class provides to build SQL queries, including SELECT, INSERT, UPDATE, and DELETE statements. 
    """

    @staticmethod
    def _format_value(value):
        if value is None:
            return 'NULL'
        return f"'{str(value)}'"

    @staticmethod
    def _format_where(where):
        if not where:
            return ''
        conditions = []
        for k, v in where.items():
            conditions.append(f"{k}={SQLQueryBuilder._format_value(v)}")
        return " WHERE " + " AND ".join(conditions)

    @staticmethod
    def select(table, columns='*', where=None):
        if columns == '*' or columns is None:
            cols = '*'
        elif isinstance(columns, (list, tuple)):
            cols = ', '.join(columns)
        else:
            cols = str(columns)
        query = f"SELECT {cols} FROM {table}"
        if where:
            query += SQLQueryBuilder._format_where(where)
        return query

    @staticmethod
    def insert(table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(SQLQueryBuilder._format_value(v)
                           for v in data.values())
        query = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        return query

    @staticmethod
    def delete(table, where=None):
        query = f"DELETE FROM {table}"
        if where:
            query += SQLQueryBuilder._format_where(where)
        return query

    @staticmethod
    def update(table, data, where=None):
        set_clause = ', '.join(
            f"{k}={SQLQueryBuilder._format_value(v)}" for k, v in data.items())
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            query += SQLQueryBuilder._format_where(where)
        return query
