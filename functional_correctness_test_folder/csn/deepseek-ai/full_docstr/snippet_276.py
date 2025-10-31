
class QuerySingle:
    '''
    Look for a single object
    '''

    def __init__(self, connection, object_type, url_params=None, query_params=None):
        '''
        Provide the connection and query parameters when you create the query.
        :param connection: The Connection to run the query against
        :param object_type: The type of object being queried (e.g., "user" or "group")
        :param url_params: Query qualifiers that go in the URL path (e.g., a group name when querying users)
        :param query_params: Query qualifiers that go in the query string (e.g., a domain name)
        '''
        self._connection = connection
        self._object_type = object_type
        self._url_params = url_params or {}
        self._query_params = query_params or {}
        self._result = None
        self._needs_reload = True

    def reload(self):
        '''
        Rerun the query (lazily).
        The result will contain a value on the server side that have changed since the last run.
        :return: None
        '''
        self._needs_reload = True

    def _fetch_result(self):
        '''
        Fetch the queried object.
        '''
        return self._connection.get(
            self._object_type,
            url_params=self._url_params,
            query_params=self._query_params
        )

    def result(self):
        '''
        Fetch the result, if we haven't already or if reload has been called.
        :return: the result object of the query.
        '''
        if self._needs_reload or self._result is None:
            self._result = self._fetch_result()
            self._needs_reload = False
        return self._result
