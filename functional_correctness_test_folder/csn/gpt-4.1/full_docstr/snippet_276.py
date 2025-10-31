
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
        self.connection = connection
        self.object_type = object_type
        self.url_params = url_params
        self.query_params = query_params
        self._result = None
        self._dirty = True

    def reload(self):
        '''
        Rerun the query (lazily).
        The result will contain a value on the server side that have changed since the last run.
        :return: None
        '''
        self._dirty = True

    def _fetch_result(self):
        '''
        Fetch the queried object.
        '''
        # Build the URL path
        path = f"/{self.object_type}"
        if self.url_params:
            if isinstance(self.url_params, (list, tuple)):
                path += "/" + "/".join(str(p) for p in self.url_params)
            else:
                path += "/" + str(self.url_params)
        # Assume connection has a get method: get(path, params)
        result = self.connection.get(path, params=self.query_params)
        return result

    def result(self):
        '''
        Fetch the result, if we haven't already or if reload has been called.
        :return: the result object of the query.
        '''
        if self._dirty or self._result is None:
            self._result = self._fetch_result()
            self._dirty = False
        return self._result
