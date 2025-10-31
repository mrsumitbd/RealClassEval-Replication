
class PlainName:

    def __init__(self, multi_metamodel_support=True):
        '''
        the default scope provider constructor
        Args:
            multi_metamodel_support: enable a AST based search, instead
            of using the parser._instances
        '''
        self.multi_metamodel_support = multi_metamodel_support

    def __call__(self, obj, attr, obj_ref):
        '''
        the default scope provider
        Args:
            obj: unused (used for multi_metamodel_support)
            attr: unused
            obj_ref: the cross reference to be resolved
        Returns:
            the resolved reference or None
        '''
        if self.multi_metamodel_support:
            # AST-based search: walk up the parent chain and look for a child with the given name
            current = obj
            name = obj_ref
            while current is not None:
                # Check all attributes of current for a matching name
                for attr_name in dir(current):
                    if attr_name.startswith('_'):
                        continue
                    value = getattr(current, attr_name)
                    if isinstance(value, list):
                        for item in value:
                            if hasattr(item, 'name') and getattr(item, 'name', None) == name:
                                return item
                    else:
                        if hasattr(value, 'name') and getattr(value, 'name', None) == name:
                            return value
                current = getattr(current, 'parent', None)
            return None
        else:
            # Use parser._instances if available
            parser = getattr(obj, 'parser', None)
            if parser is not None and hasattr(parser, '_instances'):
                for instance in parser._instances:
                    if hasattr(instance, 'name') and getattr(instance, 'name', None) == obj_ref:
                        return instance
            return None

    @classmethod
    def _inner_resolve_link_rule_ref(cls, obj_name):
        '''
        Depth-first resolving of link rule reference.
        '''
        # This is a stub for depth-first resolving, as no context is given.
        # In a real implementation, this would traverse a model tree.
        # Here, we just return None.
        return None
