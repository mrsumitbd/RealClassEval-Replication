class DatabaseSchemaIntrospectionSearchPathContext:
    """
    This context manager restores the original search path of the cursor
    once the method of the introspection class has been called.
    """

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        self.original_search_path = None

    def __enter__(self):
        self.cursor.execute('SHOW search_path')
        self.original_search_path = [search_path.strip().replace('"', '') for search_path in self.cursor.fetchone()[0].split(',')]
        self.cursor.execute(f"SET search_path = '{self.connection.schema_name}'")

    def __exit__(self, *args, **kwargs):
        formatted_search_paths = ', '.join((f"'{search_path}'" for search_path in self.original_search_path))
        self.cursor.execute(f'SET search_path = {formatted_search_paths}')