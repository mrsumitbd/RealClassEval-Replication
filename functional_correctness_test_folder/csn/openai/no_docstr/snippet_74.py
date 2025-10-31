
class PlainName:
    def __init__(self, multi_metamodel_support=True):
        """
        Initialize the PlainName resolver.

        Parameters
        ----------
        multi_metamodel_support : bool, optional
            If True, the resolver can handle references that span multiple
            metamodels. Default is True.
        """
        self.multi_metamodel_support = multi_metamodel_support

    def __call__(self, obj, attr, obj_ref):
        """
        Resolve an attribute reference on an object reference.

        Parameters
        ----------
        obj : Any
            The object that owns the attribute (unused in this simple resolver).
        attr : str or None
            The name of the attribute to resolve. If None, the whole object
            reference is returned.
        obj_ref : Any
            The object reference on which the attribute lookup should be
            performed.

        Returns
        -------
        Any
            The resolved attribute value or the original object reference if
            `attr` is None. If the attribute does not exist, None is returned.
        """
        if attr is None:
            return obj_ref
        try:
            return getattr(obj_ref, attr)
        except AttributeError:
            return None

    def _inner_resolve_link_rule_ref(self, cls, obj_name):
        """
        Resolve a link rule reference by name on a given class.

        Parameters
        ----------
        cls : type
            The class on which to look for the link rule.
        obj_name : str
            The name of the link rule to resolve.

        Returns
        -------
        Any
            The attribute or method found on the class, or None if not found.
        """
        return getattr(cls, obj_name, None)
