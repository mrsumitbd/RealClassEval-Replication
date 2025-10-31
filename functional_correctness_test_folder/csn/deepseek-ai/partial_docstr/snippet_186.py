
class TnsFilter:

    def __init__(self, *tns):
        self._tns = set(tns)

    def add(self, *tns):
        self._tns.update(tns)

    def match(self, root, ns):
        '''
        Match by I{targetNamespace} excluding those that
        are equal to the specified namespace to prevent
        adding an import to itself.
        @param root: A schema root.
        @type root: L{Element}
        '''
        tns = root.get('targetNamespace')
        return tns in self._tns and tns != ns
