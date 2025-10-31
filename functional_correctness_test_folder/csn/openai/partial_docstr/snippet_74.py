
class PlainName:
    _registry = {}

    def __init__(self, multi_metamodel_support=True):
        """
        the default scope provider constructor
        Args:
            multi_metamodel_support: enable a AST based search, instead
            of using the parser._instances
        """
        self.multi_metamodel_support = multi_metamodel_support

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
        # If the reference is already a resolved object, return it
        if isinstance(obj_ref, (str, int, float)):
            return obj_ref

        # If the reference is a dict with a 'name' key, return the name
        if isinstance(obj_ref, dict) and 'name' in obj_ref:
            return obj_ref['name']

        # If multi_metamodel_support is enabled, attempt a simple AST-like search
        if self.multi_metamodel_support:
            # Simulate an AST search by looking for a 'name' attribute
            if hasattr(obj_ref, 'name'):
                return getattr(obj_ref, 'name')
            # If obj_ref is a list or tuple, search recursively
            if isinstance(obj_ref, (list, tuple)):
                for item in obj_ref:
                    result = self.__call__(obj, attr, item)
                    if result is not None:
                        return result

        # Fallback: try to resolve via the registry
        if isinstance(obj_ref, str):
            return self._inner_resolve_link_rule_ref(self, obj_ref)

        return None

    def _inner_resolve_link_rule_ref(self, cls, obj_name):
        """
        Depth-first resolving of link rule reference.
        """
        # Simple depth-first search in the registry
        visited = set()

        def dfs(name):
            if name in visited:
                return None
            visited.add(name)
            entry = cls._registry.get(name)
            if entry is None:
                return None
            # If the entry is a reference to another name, resolve it
            if isinstance(entry, str) and entry != name:
                return dfs(entry)
            return entry

        return dfs(obj_name)
