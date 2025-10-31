
class Exporter:

    def __init__(self, globls):
        self.globls = globls
        self.tracked_instances = {}

    def export(self, defn):
        if isinstance(defn, type):
            self.tracked_instances[defn.__name__] = defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self.original_globals = self.globls.copy()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        for key, value in self.globls.items():
            if key not in self.original_globals:
                self.export(value)
