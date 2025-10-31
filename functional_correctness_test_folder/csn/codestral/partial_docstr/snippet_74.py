
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
            # Implement AST based search
            pass
        else:
            # Implement search using parser._instances
            pass

    def _inner_resolve_link_rule_ref(cls, obj_name):
        '''
        Depth-first resolving of link rule reference.
        '''
        pass
