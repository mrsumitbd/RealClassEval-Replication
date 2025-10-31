class SQLQueryBuilder:
    """
    This class provides to build SQL queries, including SELECT, INSERT, UPDATE, and DELETE statements. 
    """

    @staticmethod
    def _quote_value(value):
        if value is None:
            return "NULL"
        s = str(value).replace("'", "''")
        return f"'{s}'"

    @staticmethod
    def _format_columns(columns):
        if not columns or columns == '*':
            return '*'
        if isinstance(columns, (list, tuple)):
            return ', '.join(map(str, columns))
        return str(columns)

    @staticmethod
    def _format_where(where):
        if not where:
            return ''
        parts = [
            f"{k}={SQLQueryBuilder._quote_value(v)}" for k, v in where.items()]
        return ' WHERE ' + ' AND '.join(parts)

    @staticmethod
    def select(table, columns='*', where=None):
        cols = SQLQueryBuilder._format_columns(columns)
        where_clause = SQLQueryBuilder._format_where(where)
        return f"SELECT {cols} FROM {table}{where_clause}"

    @staticmethod
    def insert(table, data):
        if not data:
            raise ValueError("data must not be empty")
        cols = ', '.join(data.keys())
        vals = ', '.join(SQLQueryBuilder._quote_value(v)
                         for v in data.values())
        return f"INSERT INTO {table} ({cols}) VALUES ({vals})"

    @staticmethod
    def delete(table, where=None):
        where_clause = SQLQueryBuilder._format_where(where)
        return f"DELETE FROM {table}{where_clause}"

    @staticmethod
    def update(table, data, where=None):
        if not data:
            raise ValueError("data must not be empty")
        set_clause = ', '.join(
            f"{k}={SQLQueryBuilder._quote_value(v)}" for k, v in data.items())
        where_clause = SQLQueryBuilder._format_where(where)
        return f"UPDATE {table} SET {set_clause}{where_clause}"
