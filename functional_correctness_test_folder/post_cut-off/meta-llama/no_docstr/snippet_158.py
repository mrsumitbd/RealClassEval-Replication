
from typing import List, Dict, Any


class AWSComponentRegistry:

    def __init__(self):
        self.categories = self._discover_categories()
        self.components = self._discover_components()
        self.aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        # For demonstration purposes, assume categories are hardcoded
        return ['compute', 'storage', 'database']

    def _discover_components(self) -> Dict[str, List[str]]:
        # For demonstration purposes, assume components are hardcoded
        return {
            'compute': ['EC2', 'Lambda', 'ECS'],
            'storage': ['S3', 'EBS', 'EFS'],
            'database': ['RDS', 'DynamoDB', 'Aurora']
        }

    def _build_aliases(self) -> Dict[str, str]:
        # For demonstration purposes, assume aliases are hardcoded
        return {
            'ec2': 'EC2',
            'lambda': 'Lambda',
            's3': 'S3',
            'rds': 'RDS'
        }

    def get_node(self, node_type: str) -> Any:
        # For demonstration purposes, assume node retrieval is based on aliases
        node_type = node_type.lower()
        if node_type in self.aliases:
            node_type = self.aliases[node_type]
        for category, components in self.components.items():
            if node_type in components:
                # For demonstration purposes, assume node is an instance of a class
                # Replace with actual node class and instantiation logic
                return type(node_type, (), {})()
        raise ValueError(f"Unknown node type: {node_type}")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category:
            category = category.lower()
            if category in [cat.lower() for cat in self.categories]:
                for cat, components in self.components.items():
                    if cat.lower() == category:
                        return {cat: components}
            else:
                raise ValueError(f"Unknown category: {category}")
        return self.components


# Example usage:
if __name__ == "__main__":
    registry = AWSComponentRegistry()
    print(registry.list_available_components())
    print(registry.list_available_components('compute'))
    print(registry.get_node('ec2'))
