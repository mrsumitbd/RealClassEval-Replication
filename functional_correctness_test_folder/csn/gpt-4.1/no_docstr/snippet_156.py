
class SimpleService:

    def __init__(self, service_node):
        self.service_node = service_node

    def is_resolver(self):
        return hasattr(self.service_node, 'resolve') and callable(getattr(self.service_node, 'resolve'))
