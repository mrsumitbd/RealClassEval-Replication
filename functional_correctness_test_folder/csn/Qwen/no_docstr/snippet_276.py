
class QuerySingle:

    def __init__(self, connection, object_type, url_params=None, query_params=None):
        self.connection = connection
        self.object_type = object_type
        self.url_params = url_params if url_params is not None else {}
        self.query_params = query_params if query_params is not None else {}
        self._result = None

    def reload(self):
        self._fetch_result()

    def _fetch_result(self):
        # Assuming the connection has a method to fetch data
        self._result = self.connection.fetch(
            self.object_type, self.url_params, self.query_params)

    def result(self):
        if self._result is None:
            self._fetch_result()
        return self._result
