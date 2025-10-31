
class PlainName:

    def __init__(self, multi_metamodel_support=True):
        '''
        the default scope provider constructor
        Args:
            multi_metamodel_support: enable a AST based search, instead
            of using the parser._instances
        '''
        self.multi_metamodel_support = multi_metamodel_support
        self.parser_instances = {}  # assuming this is where parser._instances is stored

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
            return self._inner_resolve_link_rule_ref(type(obj), obj_ref)
        else:
            return self.parser_instances.get(obj_ref)

    def _inner_resolve_link_rule_ref(self, cls, obj_name):
        '''
        Depth-first resolving of link rule reference.
        '''
        if cls.__name__ == obj_name:
            return cls
        for base_cls in cls.__bases__:
            resolved_ref = self._inner_resolve_link_rule_ref(
                base_cls, obj_name)
            if resolved_ref is not None:
                return resolved_ref
        return None
