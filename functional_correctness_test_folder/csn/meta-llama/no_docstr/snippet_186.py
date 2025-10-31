
class TnsFilter:

    def __init__(self, *tns):
        self.tns = set(tns)

    def add(self, *tns):
        self.tns.update(tns)

    def match(self, root, ns):
        return root.tag.split('}')[-1] in self.tns or ns in self.tns
