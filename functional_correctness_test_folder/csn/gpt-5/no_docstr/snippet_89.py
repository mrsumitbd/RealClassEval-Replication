class Loader:

    def __init__(self, name, get_pipeline_definition):
        if not callable(get_pipeline_definition):
            raise TypeError("get_pipeline_definition must be callable")
        self.name = name
        self._get_pipeline_definition = get_pipeline_definition
        self._cache = {}
        try:
            from threading import RLock
        except Exception:
            self._lock = None
        else:
            self._lock = RLock()

    def clear(self):
        if self._lock:
            with self._lock:
                self._cache.clear()
        else:
            self._cache.clear()

    def get_pipeline(self, name, parent):
        key = (parent, name)
        if self._lock:
            with self._lock:
                if key in self._cache:
                    return self._cache[key]
                pipeline = self._load_pipeline(name, parent)
                self._cache[key] = pipeline
                return pipeline
        else:
            if key in self._cache:
                return self._cache[key]
            pipeline = self._load_pipeline(name, parent)
            self._cache[key] = pipeline
            return pipeline

    def _load_pipeline(self, name, parent):
        pipeline = self._get_pipeline_definition(name, parent)
        if pipeline is None:
            raise ValueError(
                f"Pipeline '{name}' could not be loaded by loader '{self.name}'")
        return pipeline
