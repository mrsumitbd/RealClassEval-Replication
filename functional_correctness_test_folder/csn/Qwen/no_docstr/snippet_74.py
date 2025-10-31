
class PlainName:

    def __init__(self, multi_metamodel_support=True):
        self.multi_metamodel_support = multi_metamodel_support

    def __call__(self, obj, attr, obj_ref):
        return self._inner_resolve_link_rule_ref(obj_ref)

    def _inner_resolve_link_rule_ref(self, obj_name):
        # Placeholder implementation
        return f"Resolved {obj_name}"
