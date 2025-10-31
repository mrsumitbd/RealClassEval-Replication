
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
        self.url_params = url_params or []
        self.query_params = query_params or {}
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
        # Build the URL path
        path_parts = [self.object_type]
        if isinstance(self.url_params, (list, tuple)):
            path_parts.extend(str(p) for p in self.url_params)
        else:
            path_parts.append(str(self.url_params))
        path = '/' + '/'.join(path_parts)

        # Perform the GET request
        response = self.connection.get(path, params=self.query_params)

        # Basic error handling
        if not hasattr(response, 'status_code') or response.status_code != 200:
            raise RuntimeError(
                f'Query failed with status {getattr(response, "status_code", None)}')

        # Parse JSON
        if hasattr(response, 'json'):
            data = response.json()
        else:
            # Fallback if response is already a dict
            data = response

        return data

    def result(self):
        '''
        Fetch the result, if we haven't already or if reload has been called.
        :return: the result object of the query.
        '''
        if self._needs_reload or self._result is None:
            self._result = self._fetch_result()
            self._needs_reload = False
        return self._result
