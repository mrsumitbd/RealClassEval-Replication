class DAVResolver:
    """Return a DAVResource object for a path (None, if not found)."""

    def __init__(self, parent_resolver, name):
        self.parent_resolver = parent_resolver
        self.name = name

    def resolve(self, script_name, path_info, environ):
        raise NotImplementedError