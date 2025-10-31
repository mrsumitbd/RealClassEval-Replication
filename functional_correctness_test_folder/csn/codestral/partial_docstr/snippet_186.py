
class TnsFilter:

    def __init__(self, *tns):
        self.tns = set(tns)

    def add(self, *tns):
        self.tns.update(tns)

    def match(self, root, ns):
        '''
        Match by I{targetNamespace} excluding those that
        are equal to the specified namespace to prevent
        adding an import to itself.
        @param root: A schema root.
        @type root: L{Element}
        '''
        if root.attrib.get('targetNamespace') in self.tns and root.attrib.get('targetNamespace') != ns:
            return True
        return False
