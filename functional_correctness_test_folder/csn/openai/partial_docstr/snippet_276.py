
import json
from urllib.parse import urlencode


class QuerySingle:
    """
    A helper class to fetch a single object from a REST‑style API.

    Parameters
    ----------
    connection : object
        An object that knows how to perform HTTP requests.  It must expose
        either a ``get(url, params=None)`` method that returns a
        ``requests.Response``‑like object, or a ``query_single`` method
        that accepts ``object_type``, ``url_params`` and ``query_params``.
    object_type : str or type
        The endpoint name (e.g. ``"users"``) or a class that can be
        instantiated from the JSON payload.
    url_params : dict, optional
        Parameters that are appended to the URL path.  For example,
        ``{"id": 42}`` will result in ``/users/42``.
    query_params : dict, optional
        Query string parameters.
    """

    def __init__(self, connection, object_type, url_params=None, query_params=None):
        self.connection = connection
        self.object_type = object_type
        self.url_params = url_params or {}
        self.query_params = query_params or {}
        self._result = None

    def reload(self):
        """
        Force a re‑fetch of the object from the server.
        """
        self._result = None
        return self._fetch_result()

    def _fetch_result(self):
        """
        Internal helper that performs the HTTP request and stores the
        result.  The result is either a plain dictionary or an instance
        of ``object_type`` if it is a class.
        """
        # Build the path
        path = str(self.object_type).lstrip("/")
        if self.url_params:
            # Append each value in the order of the dict
            for key, value in self.url_params.items():
                path += f"/{value}"

        # Build the full URL
        base = getattr(self.connection, "base_url", "")
        url = f"{base.rstrip('/')}/{path.lstrip('/')}"

        # Perform the request
        if hasattr(self.connection, "query_single"):
            # Custom method provided by the connection
            data = self.connection.query_single(
                self.object_type, self.url_params, self.query_params
            )
        else:
            # Fallback to a generic GET
            params = self.query_params
            resp = self.connection.get(url, params=params)
            if not hasattr(resp, "json"):
                # If the response is already a dict
                data = resp
            else:
                data = resp.json()

        # Instantiate the object if a class was supplied
        if isinstance(self.object_type, type):
            try:
                self._result = self.object_type(**data)
            except TypeError:
                # If the constructor signature doesn't match, fall back to dict
                self._result = data
        else:
            self._result = data

        return self._result

    def result(self):
        """
        Return the fetched object, fetching it lazily if necessary.
        """
        if self._result is None:
            self._fetch_result()
        return self._result
