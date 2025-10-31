
class Exporter:

    def __init__(self, globls):

        self.globls = globls

    def export(self, defn):

        if defn in self.globls:
            return self.globls[defn]
        else:
            raise ValueError(f"Definition '{defn}' not found in globals.")

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")
        return False
