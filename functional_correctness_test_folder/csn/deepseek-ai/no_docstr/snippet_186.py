
class TnsFilter:

    def __init__(self, *tns):
        self._tns = set(tns)

    def add(self, *tns):
        self._tns.update(tns)

    def match(self, root, ns):
        return ns in self._tns
