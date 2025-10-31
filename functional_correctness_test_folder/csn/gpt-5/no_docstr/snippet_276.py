class QuerySingle:

    def __init__(self, connection, object_type, url_params=None, query_params=None):
        self._connection = connection
        self._object_type = object_type
        self._url_params = url_params or {}
        self._query_params = query_params or {}
        self._result = None
        self._loaded = False

    def reload(self):
        self._loaded = False
        self._result = None
        return self.result()

    def _fetch_result(self):
        path = None

        if hasattr(self._object_type, "endpoint"):
            path = getattr(self._object_type, "endpoint")
        elif isinstance(self._object_type, str):
            path = self._object_type
        else:
            name = getattr(self._object_type, "__name__",
                           str(self._object_type))
            path = name.lower()

        if isinstance(path, str) and self._url_params:
            try:
                path = path.format(**self._url_params)
            except Exception:
                pass  # leave path as-is if formatting fails

        data = None
        conn = self._connection

        if hasattr(conn, "request"):
            data = conn.request("GET", path, params=self._query_params)
        elif hasattr(conn, "get"):
            try:
                data = conn.get(path, params=self._query_params)
            except TypeError:
                data = conn.get(path, self._query_params)
        elif callable(conn):
            try:
                data = conn(path, self._query_params)
            except TypeError:
                data = conn(path)
        else:
            raise TypeError("Unsupported connection interface")

        obj = data
        typ = self._object_type

        if hasattr(typ, "from_dict") and callable(getattr(typ, "from_dict")):
            obj = typ.from_dict(data)
        elif hasattr(typ, "from_json") and callable(getattr(typ, "from_json")):
            obj = typ.from_json(data)
        elif callable(typ) and not isinstance(typ, str):
            try:
                obj = typ(data)
            except TypeError:
                obj = typ()

        self._result = obj
        self._loaded = True

    def result(self):
        if not self._loaded:
            self._fetch_result()
        return self._result
