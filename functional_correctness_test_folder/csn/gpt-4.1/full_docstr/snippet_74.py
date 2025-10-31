
class PlainName:
    '''
    plain name scope provider
    '''

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
        if obj_ref is None or not hasattr(obj_ref, 'name'):
            return None

        obj_name = obj_ref.name

        if self.multi_metamodel_support:
            # AST-based search: walk up the parent chain to find a matching name
            current = obj_ref
            while hasattr(current, 'parent') and current.parent is not None:
                parent = current.parent
                # Search all children of parent for a matching name
                for child in getattr(parent, 'children', []):
                    if hasattr(child, 'name') and child.name == obj_name:
                        return child
                current = parent
            # If not found, try the root
            root = obj_ref
            while hasattr(root, 'parent') and root.parent is not None:
                root = root.parent
            # Search all children of root
            for child in getattr(root, 'children', []):
                if hasattr(child, 'name') and child.name == obj_name:
                    return child
            return None
        else:
            # Use parser._instances if available
            parser = getattr(obj_ref, 'parser', None)
            if parser is not None and hasattr(parser, '_instances'):
                for instance in parser._instances:
                    if hasattr(instance, 'name') and instance.name == obj_name:
                        return instance
            return None

    @classmethod
    def _inner_resolve_link_rule_ref(cls, obj_name):
        '''
        Depth-first resolving of link rule reference.
        '''
        # This is a stub, as the context is not fully defined.
        # In a real implementation, this would perform a depth-first search
        # in a rule registry or similar structure.
        return None
