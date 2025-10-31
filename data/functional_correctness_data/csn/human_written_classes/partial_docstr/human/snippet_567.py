from packaging.version import Version
from collections import OrderedDict

class Api:
    """
    A full description of an API's namespaces, data types, and routes.
    """

    def __init__(self, version):
        self.version = Version(version)
        self.namespaces = OrderedDict()
        self.route_schema = None

    def ensure_namespace(self, name):
        """
        Only creates a namespace if it hasn't yet been defined.

        :param str name: Name of the namespace.

        :return ApiNamespace:
        """
        if name not in self.namespaces:
            self.namespaces[name] = ApiNamespace(name)
        return self.namespaces[name]

    def normalize(self):
        """
        Alphabetizes namespaces and routes to make spec parsing order mostly
        irrelevant.
        """
        ordered_namespaces = OrderedDict()
        for namespace_name in sorted(self.namespaces.keys()):
            ordered_namespaces[namespace_name] = self.namespaces[namespace_name]
        self.namespaces = ordered_namespaces
        for namespace in self.namespaces.values():
            namespace.normalize()

    def add_route_schema(self, route_schema):
        assert self.route_schema is None
        self.route_schema = route_schema