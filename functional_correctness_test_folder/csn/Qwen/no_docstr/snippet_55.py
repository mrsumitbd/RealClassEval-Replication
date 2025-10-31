
class Exporter:

    def __init__(self, globls):
        self.globls = globls

    def export(self, defn):
        if isinstance(defn, dict):
            self.globls.update(defn)
        elif isinstance(defn, tuple) and len(defn) == 2:
            key, value = defn
            self.globls[key] = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
