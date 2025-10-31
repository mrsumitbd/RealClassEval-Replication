from textx.exceptions import TextXSemanticError

class PlainName:
    """
    plain name scope provider
    """

    def __init__(self, multi_metamodel_support=True):
        """
        the default scope provider constructor

        Args:
            multi_metamodel_support: enable a AST based search, instead
            of using the parser._instances
        """
        self.multi_metamodel_support = multi_metamodel_support
        pass

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
        from textx.const import RULE_ABSTRACT, RULE_COMMON
        from textx.model import ObjCrossRef
        from textx.scoping.tools import get_parser
        if obj_ref is None:
            return None
        assert type(obj_ref) is ObjCrossRef, type(obj_ref)
        if get_parser(obj).debug:
            get_parser(obj).dprint(f'Resolving obj crossref: {obj_ref.cls}:{obj_ref.obj_name}')

        def _inner_resolve_link_rule_ref(cls, obj_name):
            """
            Depth-first resolving of link rule reference.
            """
            if cls._tx_type is RULE_ABSTRACT:
                for inherited in cls._tx_inh_by:
                    result = _inner_resolve_link_rule_ref(inherited, obj_name)
                    if result:
                        return result
            elif cls._tx_type == RULE_COMMON and id(cls) in get_parser(obj)._instances:
                objs = get_parser(obj)._instances[id(cls)]
                return objs.get(obj_name)
        if self.multi_metamodel_support:
            from textx import get_children, get_model, textx_isinstance
            result_lst = get_children(lambda x: hasattr(x, 'name') and x.name == obj_ref.obj_name and textx_isinstance(x, obj_ref.cls), get_model(obj))
            if len(result_lst) == 1:
                result = result_lst[0]
            elif len(result_lst) > 1:
                line, col = get_parser(obj).pos_to_linecol(obj_ref.position)
                raise TextXSemanticError(f'name {obj_ref.obj_name} is not unique.', line=line, col=col, filename=get_model(obj)._tx_filename)
            else:
                result = None
        else:
            result = _inner_resolve_link_rule_ref(obj_ref.cls, obj_ref.obj_name)
        return result