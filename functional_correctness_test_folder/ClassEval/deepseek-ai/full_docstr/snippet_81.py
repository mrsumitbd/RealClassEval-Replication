
class SQLQueryBuilder:
    """
    This class provides to build SQL queries, including SELECT, INSERT, UPDATE, and DELETE statements. 
    """

    @staticmethod
    def select(table, columns='*', where=None):
        if isinstance(columns, list):
            columns = ', '.join(columns)
        query = f"SELECT {columns} FROM {table}"
        if where:
            conditions = ' AND '.join([f"{k}='{v}'" for k, v in where.items()])
            query += f" WHERE {conditions}"
        return query

    @staticmethod
    def insert(table, data):
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{v}'" for v in data.values()])
        return f"INSERT INTO {table} ({columns}) VALUES ({values})"

    @staticmethod
    def delete(table, where=None):
        query = f"DELETE FROM {table}"
        if where:
            conditions = ' AND '.join([f"{k}='{v}'" for k, v in where.items()])
            query += f" WHERE {conditions}"
        return query

    @staticmethod
    def update(table, data, where=None):
        set_clause = ', '.join([f"{k}='{v}'" for k, v in data.items()])
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            conditions = ' AND '.join([f"{k}='{v}'" for k, v in where.items()])
            query += f" WHERE {conditions}"
        return query
