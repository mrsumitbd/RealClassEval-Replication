
class TnsFilter:
    """
    A simple filter for target namespaces (TNS).  It stores a set of namespace
    strings and can be queried to see if a given namespace or the namespace of
    an XML element matches any of the stored values.

    The filter accepts a wildcard '*' which matches any namespace.
    """

    def __init__(self, *tns):
        """
        Initialise the filter with zero or more namespace strings.

        Parameters
        ----------
        *tns : str
            Namespace strings to initialise the filter with.
        """
        self._tns = set(tns)

    def add(self, *tns):
        """
        Add one or more namespace strings to the filter.

        Parameters
        ----------
        *tns : str
            Namespace strings to add.
        """
        self._tns.update(tns)

    def _extract_ns(self, tag):
        """
        Extract the namespace from an XML tag string.

        Parameters
        ----------
        tag : str
            The tag string, e.g. '{http://example.com}local'.

        Returns
        -------
        str or None
            The namespace URI if present, otherwise None.
        """
        if isinstance(tag, str) and tag.startswith('{'):
            end = tag.find('}')
            if end != -1:
                return tag[1:end]
        return None

    def match(self, root, ns):
        """
        Determine whether the supplied namespace or the namespace of the
        supplied root element matches any of the stored namespaces.

        Parameters
        ----------
        root : xml.etree.ElementTree.Element or str or None
            The root element (or its tag string) whose namespace may be
            checked.  If None, only the supplied `ns` is considered.
        ns : str or None
            A namespace string to check against the filter.

        Returns
        -------
        bool
            True if a match is found, False otherwise.
        """
        # Wildcard matches everything
        if '*' in self._tns:
            return True

        # Check the explicit namespace argument
        if ns is not None and ns in self._tns:
            return True

        # Check the namespace of the root element/tag
        if root is not None:
            # If root is an Element, get its tag
            tag = getattr(root, 'tag', None)
            if tag is None:
                # If root itself is a string, treat it as a tag
                tag = root
            ns_root = self._extract_ns(tag)
            if ns_root is not None and ns_root in self._tns:
                return True

        return False
