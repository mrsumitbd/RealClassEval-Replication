
class PlainName:
    """
    plain name scope provider
    """

    # Simple global registry for demo purposes
    _registry = {}

    def __init__(self, multi_metamodel_support=True):
        """
        the default scope provider constructor
        Args:
            multi_metamodel_support: enable a AST based search, instead
            of using the parser._instances
        """
        self.multi_metamodel_support = multi_metamodel_support

    @classmethod
    def register(cls, name, obj):
        """
        Register an object under a given name.
        """
        cls._registry[name] = obj

    @classmethod
    def unregister(cls, name):
        """
        Unregister an object by name.
        """
        cls._registry.pop(name, None)

    def __call__(self, obj, attr, obj_ref):
        """
        the default scope provider
        Args:
            obj: unused (used for multi_metamodel_support)
            attr: unused
            obj_ref: the cross reference to be resolved
        Returns:
            the resolved reference or None
        """
        # If obj_ref is already a resolved object, return it
        if not isinstance(obj_ref, str):
            return obj_ref

        # Resolve by name from the registry
        return self._registry.get(obj_ref)

    def _inner_resolve_link_rule_ref(self, cls, obj_name):
        """
        Depth-first resolving of link rule reference.
        """
        # If the class itself has the attribute, return it
        if hasattr(cls, obj_name):
            return getattr(cls, obj_name)

        # Recursively search base classes
        for base in cls.__bases__:
            result = self._inner_resolve_link_rule_ref(base, obj_name)
            if result is not None:
                return result

        # Not found
        return None
