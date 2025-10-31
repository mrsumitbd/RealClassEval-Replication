
class PlainName:

    def __init__(self, multi_metamodel_support=True):
        self.multi_metamodel_support = multi_metamodel_support

    def __call__(self, obj, attr, obj_ref):
        return self._inner_resolve_link_rule_ref(obj_ref.__class__, obj_ref.name)

    def _inner_resolve_link_rule_ref(self, cls, obj_name):
        return obj_name
