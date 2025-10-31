
class Exporter:

    def __init__(self, globls):

        self.globls = globls
        self.tracked_instances = []

    def export(self, defn):

        if defn in self.globls:
            instance = self.globls[defn]()
            self.tracked_instances.append(instance)
            return instance
        else:
            raise ValueError(f"Definition {defn} not found in globals.")

    def __enter__(self):

        self.tracked_instances = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.tracked_instances = []
