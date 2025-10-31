
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
        # Assuming the connection object has a method to make a GET request
        self._result = self.connection.get(
            self.object_type, url_params=self.url_params, query_params=self.query_params)
        self._dirty = False

    def result(self):
        '''
        Fetch the result, if we haven't already or if reload has been called.
        :return: the result object of the query.
        '''
        if self._dirty:
            self._fetch_result()
        return self._result
