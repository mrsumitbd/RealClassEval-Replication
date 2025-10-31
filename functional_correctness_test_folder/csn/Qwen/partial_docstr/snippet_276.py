
class QuerySingle:

    def __init__(self, connection, object_type, url_params=None, query_params=None):
        self.connection = connection
        self.object_type = object_type
        self.url_params = url_params if url_params is not None else {}
        self.query_params = query_params if query_params is not None else {}
        self._result = None

    def reload(self):
        self._result = self._fetch_result()

    def _fetch_result(self):
        '''
        Fetch the queried object.
        '''
        # Assuming the connection has a method to fetch data
        response = self.connection.fetch(
            self.object_type, self.url_params, self.query_params)
        return response.get('data', None)

    def result(self):
        if self._result is None:
            self.reload()
        return self._result
