class TaskConfiguration:

    def __init__(self):
        self._namespaces = []

    def create_namespace(self, namespace):
        namespace = TaskNamespace(namespace, self)
        self._namespaces.append(namespace)
        return namespace

    @property
    def namespaces(self):
        return list(self._namespaces)