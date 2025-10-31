
class Exporter:

    def __init__(self, globls):
        self.globls = globls
        self.original_globals = globls.copy()

    def export(self, defn):
        self.globls.update(defn)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.globls.clear()
        self.globls.update(self.original_globals)
