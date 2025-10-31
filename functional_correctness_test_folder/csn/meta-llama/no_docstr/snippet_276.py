
import requests


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
        url = self.connection.base_url + '/' + \
            self.object_type.format(**self.url_params)
        response = requests.get(
            url, params=self.query_params, auth=self.connection.auth)
        response.raise_for_status()
        return response.json()

    def result(self):
        if self._result is None:
            self.reload()
        return self._result
