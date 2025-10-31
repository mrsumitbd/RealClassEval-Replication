class TnsFilter:
    def __init__(self, *tns):
        """Create a filter for target namespaces.

        Parameters
        ----------
        *tns : str
            Target namespaces to filter.
        """
        self._tns = set(tns)

    def add(self, *tns):
        """Add more target namespaces to the filter.

        Parameters
        ----------
        *tns : str
            Target namespaces to add.
        """
        self._tns.update(tns)

    def match(self, root, ns):
        """
        Match by targetNamespace excluding those that are equal to the
        specified namespace to prevent adding an import to itself.

        Parameters
        ----------
        root : Element
            A schema root element.
        ns : str
            The namespace to exclude (typically the current schema's namespace).

        Returns
        -------
        bool
            True if the root's targetNamespace is in the filter and not equal to `ns`,
            False otherwise.
        """
        if root is None:
            return False
        target_ns = root.attrib.get('targetNamespace')
        if not target_ns:
            return False
        if target_ns == ns:
            return False
        return target_ns in self._tns
