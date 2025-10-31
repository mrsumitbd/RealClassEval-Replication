class TnsFilter:
    '''
    Target Namespace filter.
    @ivar tns: A list of target namespaces.
    @type tns: [str,...]
    '''

    def __init__(self, *tns):
        '''
        @param tns: A list of target namespaces.
        @type tns: [str,...]
        '''
        self.tns = []
        self._tns_set = set()
        if tns:
            self.add(*tns)

    def add(self, *tns):
        '''
        Add targetNamesapces to be added.
        @param tns: A list of target namespaces.
        @type tns: [str,...]
        '''
        # Support passing a single iterable like list/tuple/set
        if len(tns) == 1 and isinstance(tns[0], (list, tuple, set)):
            tns_iter = tns[0]
        else:
            tns_iter = tns

        for item in tns_iter:
            if item is None:
                continue
            s = str(item)
            if not s:
                continue
            if s not in self._tns_set:
                self._tns_set.add(s)
                self.tns.append(s)

    def match(self, root, ns):
        '''
        Match by targetNamespace excluding those that
        are equal to the specified namespace to prevent
        adding an import to itself.
        @param root: A schema root.
        @type root: L{Element}
        '''
        if root is None:
            return False

        # Try to obtain the targetNamespace from element
        tns_value = None
        if hasattr(root, 'get'):
            tns_value = root.get('targetNamespace')
        if tns_value is None and hasattr(root, 'attrib'):
            tns_value = root.attrib.get('targetNamespace')

        if not tns_value:
            return False
        if ns is not None and tns_value == ns:
            return False

        if not self._tns_set:
            return True

        return tns_value in self._tns_set
