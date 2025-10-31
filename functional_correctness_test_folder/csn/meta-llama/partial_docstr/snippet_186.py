
from xml.etree import ElementTree as ET


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
        tns = root.attrib.get('targetNamespace')
        return tns in self.tns and tns != ns
