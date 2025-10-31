
class PlainName:

    def __init__(self, multi_metamodel_support=True):
        self.multi_metamodel_support = multi_metamodel_support

    def __call__(self, obj, attr, obj_ref):
        return getattr(obj, attr, None)

    def _inner_resolve_link_rule_ref(cls, obj_name):
        return obj_name
