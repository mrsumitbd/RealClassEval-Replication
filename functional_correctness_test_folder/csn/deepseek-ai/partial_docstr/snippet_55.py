
class Exporter:

    def __init__(self, globls):
        self.globls = globls
        self.tracked_instances = []
        self._in_context = False

    def export(self, defn):
        if self._in_context:
            self.tracked_instances.append(defn)
        self.globls[defn.__name__] = defn

    def __enter__(self):
        self._in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._in_context = False
