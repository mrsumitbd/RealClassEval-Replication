class QuerySingle:
    """
    Look for a single object
    """

    def __init__(self, connection, object_type, url_params=None, query_params=None):
        """
        Provide the connection and query parameters when you create the query.

        :param connection: The Connection to run the query against
        :param object_type: The type of object being queried (e.g., "user" or "group")
        :param url_params: Query qualifiers that go in the URL path (e.g., a group name when querying users)
        :param query_params: Query qualifiers that go in the query string (e.g., a domain name)
        """
        self.conn = connection
        self.object_type = object_type
        self.url_params = url_params if url_params else []
        self.query_params = query_params if query_params else {}
        self._result = None

    def reload(self):
        """
        Rerun the query (lazily).
        The result will contain a value on the server side that have changed since the last run.
        :return: None
        """
        self._result = None

    def _fetch_result(self):
        """
        Fetch the queried object.
        """
        self._result = self.conn.query_single(self.object_type, self.url_params, self.query_params)

    def result(self):
        """
        Fetch the result, if we haven't already or if reload has been called.
        :return: the result object of the query.
        """
        if self._result is None:
            self._fetch_result()
        return self._result