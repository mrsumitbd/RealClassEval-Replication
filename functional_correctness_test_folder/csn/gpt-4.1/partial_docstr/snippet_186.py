
class TnsFilter:

    def __init__(self, *tns):
        self.tns_set = set(tns)

    def add(self, *tns):
        self.tns_set.update(tns)

    def match(self, root, ns):
        '''
        Match by I{targetNamespace} excluding those that
        are equal to the specified namespace to prevent
        adding an import to itself.
        @param root: A schema root.
        @type root: L{Element}
        '''
        tns = root.get('targetNamespace')
        return tns is not None and tns != ns and tns in self.tns_set
