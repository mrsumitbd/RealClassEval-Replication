
class QuerySingle:

    def __init__(self, connection, object_type, url_params=None, query_params=None):
        self.connection = connection
        self.object_type = object_type
        self.url_params = url_params or {}
        self.query_params = query_params or {}
        self._result = None

    def reload(self):
        self._result = self._fetch_result()

    def _fetch_result(self):
        '''
        Fetch the queried object.
        '''
        # Assume connection has a method get_object that takes object_type, url_params, query_params
        return self.connection.get_object(
            self.object_type,
            url_params=self.url_params,
            query_params=self.query_params
        )

    def result(self):
        if self._result is None:
            self.reload()
        return self._result
