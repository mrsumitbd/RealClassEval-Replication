class ConnectionRemover:

    def __init__(self, connection_class):
        self._connection_class = connection_class
        self._connection_pool_to_connections = {}

    def add_connection_to_pool_entry(self, pool, connection):
        if isinstance(connection, self._connection_class):
            self._connection_pool_to_connections.setdefault(pool, set()).add(connection)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for pool, connections in self._connection_pool_to_connections.items():
            readd_connections = []
            while pool.pool and (not pool.pool.empty()) and connections:
                connection = pool.pool.get()
                if isinstance(connection, self._connection_class):
                    connections.remove(connection)
                    connection.close()
                else:
                    readd_connections.append(connection)
            for connection in readd_connections:
                pool._put_conn(connection)
            for connection in connections:
                connection.close()