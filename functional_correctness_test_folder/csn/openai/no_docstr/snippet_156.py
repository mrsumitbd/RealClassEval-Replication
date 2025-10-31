class SimpleService:
    def __init__(self, service_node):
        self.service_node = service_node

    def is_resolver(self):
        # Handle dictionary-like service nodes
        if isinstance(self.service_node, dict):
            if "type" in self.service_node:
                return self.service_node["type"] == "resolver"
            if "resolver" in self.service_node:
                return bool(self.service_node["resolver"])

        # Handle object-like service nodes
        if hasattr(self.service_node, "is_resolver"):
            attr = getattr(self.service_node, "is_resolver")
            if callable(attr):
                return attr()
            return bool(attr)

        if hasattr(self.service_node, "type"):
            return getattr(self.service_node, "type") == "resolver"

        if hasattr(self.service_node, "resolver"):
            return bool(getattr(self.service_node, "resolver"))

        return False
