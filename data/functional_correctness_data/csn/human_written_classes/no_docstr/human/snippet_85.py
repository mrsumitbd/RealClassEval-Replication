class BaseNamespace:

    def __init__(self, namespace=None):
        self.namespace = namespace or '/'

    def is_asyncio_based(self):
        return False