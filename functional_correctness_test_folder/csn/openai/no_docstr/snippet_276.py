class QuerySingle:
    def __init__(self, connection, object_type, url_params=None, query_params=None):
        """
        Initialize a QuerySingle instance.

        :param connection: An object that provides a `get` method for HTTP requests.
        :param object_type: Either a class to instantiate with the fetched data or a string key.
        :param url_params: Optional dict or string to extend the URL path.
        :param query_params: Optional dict of query string parameters.
        """
        self.connection = connection
        self.object_type = object_type
        self.url_params = url_params
        self.query_params = query_params or {}
        self._result = None

    def reload(self):
        """
        Force a reload of the data from the remote source.
        """
        self._result = None
        return self._fetch_result()

    def _fetch_result(self):
        """
        Internal method to perform the HTTP GET request and parse the result.
        """
        # Build the base path
        if isinstance(self.object_type, str):
            path = f"/{self.object_type}"
        else:
            # Assume the class has a __name__ attribute
            path = f"/{self.object_type.__name__.lower()}"

        # Append URL parameters if provided
        if self.url_params:
            if isinstance(self.url_params, dict):
                # Append each value in order of insertion
                path += "/" + "/".join(str(v)
                                       for v in self.url_params.values())
            else:
                # Treat as a string path segment
                path += f"/{self.url_params}"

        # Perform the GET request
        try:
            response = self.connection.get(path, params=self.query_params)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to fetch data from {path}: {exc}") from exc

        # Raise for HTTP errors
        if hasattr(response, "raise_for_status"):
            try:
                response.raise_for_status()
            except Exception as exc:
                raise RuntimeError(
                    f"HTTP error while fetching {path}: {exc}") from exc

        # Parse JSON
        try:
            data = response.json()
        except Exception as exc:
            raise ValueError(
                f"Response from {path} is not valid JSON: {exc}") from exc

        # Instantiate object_type if it's a class
        if isinstance(self.object_type, type):
            try:
                if isinstance(data, dict):
                    result = self.object_type(**data)
                else:
                    # If data is not a dict, pass it as a single positional argument
                    result = self.object_type(data)
            except Exception as exc:
                raise ValueError(
                    f"Failed to instantiate {self.object_type} with data: {exc}") from exc
        else:
            # If object_type is not a class, just return the raw data
            result = data

        self._result = result
        return result

    def result(self):
        """
        Return the fetched result, fetching it if necessary.
        """
        if self._result is None:
            self._fetch_result()
        return self._result
