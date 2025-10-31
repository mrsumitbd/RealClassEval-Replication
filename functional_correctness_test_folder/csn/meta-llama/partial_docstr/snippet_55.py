
import inspect


class Exporter:

    def __init__(self, globls):
        self.globls = globls
        self.instances = []

    def export(self, defn):
        self.globls[defn.__name__] = defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self.prev_frame = inspect.currentframe().f_back
        self.prev_globals = self.prev_frame.f_globals
        self.prev_locals = self.prev_frame.f_locals
        self.instances.append(self.prev_globals.copy())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        current_globals = self.prev_frame.f_globals
        for name, obj in current_globals.items():
            if name not in self.instances[-1]:
                self.export(obj)
        self.instances.pop()
        del self.prev_frame
        del self.prev_globals
        del self.prev_locals
