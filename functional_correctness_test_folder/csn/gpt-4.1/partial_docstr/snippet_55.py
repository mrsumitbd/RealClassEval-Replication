
class Exporter:
    def __init__(self, globls):
        self.globls = globls
        self._tracking = False
        self._before = set()
        self._created = set()

    def export(self, defn):
        name = defn.__name__ if hasattr(defn, '__name__') else str(defn)
        self.globls[name] = defn
        return defn

    def __enter__(self):
        self._tracking = True
        self._before = set(self.globls.keys())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._tracking:
            after = set(self.globls.keys())
            self._created = after - self._before
            self._tracking = False
