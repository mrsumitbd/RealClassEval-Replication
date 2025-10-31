
class PlainName:

    def __init__(self, multi_metamodel_support=True):
        self.multi_metamodel_support = multi_metamodel_support

    def __call__(self, obj, attr, obj_ref):
        # Return the plain name of the object, which is assumed to be the 'name' attribute
        return getattr(obj, 'name', None)

    @classmethod
    def _inner_resolve_link_rule_ref(cls, obj_name):
        # Just return the object name as is
        return obj_name
