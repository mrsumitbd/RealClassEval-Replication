
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
        self.tns = list(tns)

    def add(self, *tns):
        '''
        Add I{targetNamesapces} to be added.
        @param tns: A list of target namespaces.
        @type tns: [str,...]
        '''
        self.tns.extend(tns)

    def match(self, root, ns):
        '''
        Match by I{targetNamespace} excluding those that
        are equal to the specified namespace to prevent
        adding an import to itself.
        @param root: A schema root.
        @type root: L{Element}
        '''
        target_ns = root.get('targetNamespace')
        if target_ns is None:
            return False
        return target_ns in self.tns and target_ns != ns
