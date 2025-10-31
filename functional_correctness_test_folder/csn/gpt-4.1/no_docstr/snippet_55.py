
class Exporter:

    def __init__(self, globls):
        self.globls = globls
        self._exported = []

    def export(self, defn):
        name = defn.__name__
        self.globls[name] = defn
        self._exported.append(name)
        return defn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Optionally, could remove exported names on exit, but not specified
        pass
