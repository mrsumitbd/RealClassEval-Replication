class Template:

    def __init__(self, name, versions):
        self.name = name
        if versions is None:
            raise ValueError("versions must not be None")
        if isinstance(versions, dict):
            if not versions:
                raise ValueError("versions dict must not be empty")
            self._versions = dict(versions)
        else:
            try:
                iterable = list(versions)
            except TypeError:
                raise TypeError(
                    "versions must be a dict or an iterable of version names")
            if not iterable:
                raise ValueError("versions iterable must not be empty")
            self._versions = {str(v): v for v in iterable}
        self._latest_cache = None

    def _version_key(self, ver_name):
        import re
        if not isinstance(ver_name, str):
            ver_name = str(ver_name)
        parts = []
        for token in ver_name.split('.'):
            for chunk in re.findall(r'\d+|[A-Za-z]+|[^A-Za-z\d]+', token):
                if chunk.isdigit():
                    parts.append((0, int(chunk)))
                elif chunk.isalpha():
                    parts.append((1, chunk.lower()))
                else:
                    parts.append((2, chunk))
        return tuple(parts)

    def get_version(self, ver_name=None):
        if ver_name is None:
            key = self.get_latest_version()
            return self._versions[key]
        if ver_name in self._versions:
            return self._versions[ver_name]
        # allow stringified lookup if original key types were non-strings
        sver = str(ver_name)
        if sver in self._versions:
            return self._versions[sver]
        raise KeyError(f"Version '{ver_name}' not found")

    def get_latest_version(self):
        if self._latest_cache is not None:
            return self._latest_cache
        # Determine latest by comparing version-like keys
        keys = list(self._versions.keys())
        latest = max(keys, key=self._version_key)
        self._latest_cache = latest
        return latest
