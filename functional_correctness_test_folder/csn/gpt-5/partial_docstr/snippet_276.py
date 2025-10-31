class QuerySingle:
    def __init__(self, connection, object_type, url_params=None, query_params=None):
        self.connection = connection
        self.object_type = object_type
        self.url_params = url_params or {}
        self.query_params = query_params or {}
        self._result = None

    def reload(self):
        self._result = None
        return self.result()

    def _fetch_result(self):
        '''
        Fetch the queried object.
        '''
        import inspect
        import json
        from urllib.parse import urlencode, urljoin

        # Determine endpoint/path from object_type
        endpoint = None
        if isinstance(self.object_type, str):
            endpoint = self.object_type
        else:
            endpoint = getattr(self.object_type, "endpoint", None) or getattr(
                self.object_type, "path", None)
        if not endpoint:
            raise ValueError(
                "Cannot determine endpoint/path from object_type. Provide a string endpoint or ensure object_type has 'endpoint' or 'path' attribute.")

        # Format URL with path parameters
        try:
            endpoint_formatted = endpoint.format(
                **self.url_params) if self.url_params else endpoint
        except KeyError as e:
            raise ValueError(
                f"Missing URL parameter for endpoint formatting: {e}") from e

        # Build absolute URL if connection holds a base_url, otherwise use endpoint as-is
        base_url = getattr(self.connection, "base_url", None)
        if base_url:
            url = urljoin(base_url.rstrip("/") + "/",
                          endpoint_formatted.lstrip("/"))
        else:
            url = endpoint_formatted

        # Execute GET request
        resp = None
        if hasattr(self.connection, "get") and callable(self.connection.get):
            resp = self.connection.get(url, params=self.query_params or None)
        elif hasattr(self.connection, "request") and callable(self.connection.request):
            # Common interface like requests.Session.request
            resp = self.connection.request(
                "GET", url, params=self.query_params or None)
        else:
            raise AttributeError(
                "Connection must provide a 'get' or 'request' method.")

        # Extract payload
        data = None
        if hasattr(resp, "json") and callable(resp.json):
            data = resp.json()
        elif isinstance(resp, (dict, list)):
            data = resp
        elif isinstance(resp, str):
            try:
                data = json.loads(resp)
            except json.JSONDecodeError:
                data = resp
        else:
            # Try attribute commonly used by HTTP client libraries
            content = getattr(resp, "text", None)
            if content is not None:
                try:
                    data = json.loads(content)
                except Exception:
                    data = content
            else:
                data = resp

        # Normalize to a single object
        if isinstance(data, list):
            data = data[0] if data else None

        # Construct target object
        def build_object(payload):
            if payload is None:
                return None

            # Prefer classmethod or staticmethod constructors
            if hasattr(self.object_type, "from_dict") and callable(getattr(self.object_type, "from_dict")):
                try:
                    return self.object_type.from_dict(payload)
                except Exception:
                    pass
            if hasattr(self.object_type, "from_json") and callable(getattr(self.object_type, "from_json")):
                try:
                    return self.object_type.from_json(payload)
                except Exception:
                    pass

            # If it's a class, try kwargs then single-arg
            if inspect.isclass(self.object_type):
                if isinstance(payload, dict):
                    try:
                        return self.object_type(**payload)
                    except Exception:
                        pass
                try:
                    return self.object_type(payload)
                except Exception:
                    return payload

            # If it's any callable (factory)
            if callable(self.object_type):
                try:
                    return self.object_type(payload)
                except Exception:
                    return payload

            # Fallback: return raw payload
            return payload

        return build_object(data)

    def result(self):
        if self._result is None:
            self._result = self._fetch_result()
        return self._result
