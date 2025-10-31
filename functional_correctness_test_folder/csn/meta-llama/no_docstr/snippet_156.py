
class SimpleService:

    def __init__(self, service_node):
        """
        Initialize the SimpleService instance.

        Args:
            service_node: The node representing the service.
        """
        self.service_node = service_node

    def is_resolver(self):
        """
        Check if the service is a resolver.

        Returns:
            bool: True if the service is a resolver, False otherwise.
        """
        return hasattr(self.service_node, 'resolve') and callable(self.service_node.resolve)
