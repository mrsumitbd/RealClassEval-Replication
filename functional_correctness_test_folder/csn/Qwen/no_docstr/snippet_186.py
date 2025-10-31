
class TnsFilter:

    def __init__(self, *tns):
        self.tns_set = set(tns)

    def add(self, *tns):
        self.tns_set.update(tns)

    def match(self, root, ns):
        return any(tns in ns for tns in self.tns_set)
