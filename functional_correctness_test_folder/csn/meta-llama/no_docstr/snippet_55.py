
class Exporter:

    def __init__(self, globls):
        self.globls = globls
        self.exported = set()

    def export(self, defn):
        self.globls[defn.__name__] = defn
        self.exported.add(defn.__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name in list(self.globls.keys()):
            if name.startswith('__') and name != '__all__':
                continue
            if name not in self.exported:
                del self.globls[name]
        return False
