
class TnsFilter:

    def __init__(self, *tns):
        self.tns = set(tns)

    def add(self, *tns):
        self.tns.update(tns)

    def match(self, root, ns):
        if root in self.tns:
            return True
        if ns in self.tns:
            return True
        return False
