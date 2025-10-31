
from typing import List, Dict, Any


class AWSComponentRegistry:

    def __init__(self):
        self.categories = self._discover_categories()
        self.components = self._discover_components()
        self.aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        # Simulated discovery of categories
        return ["Compute", "Storage", "Database", "Networking"]

    def _discover_components(self) -> Dict[str, List[str]]:
        # Simulated discovery of components
        return {
            "Compute": ["EC2", "Lambda", "ECS"],
            "Storage": ["S3", "EBS", "EFS"],
            "Database": ["RDS", "DynamoDB", "Redshift"],
            "Networking": ["VPC", "ELB", "CloudFront"]
        }

    def _build_aliases(self) -> Dict[str, str]:
        # Simulated building of aliases
        return {
            "Amazon EC2": "EC2",
            "AWS Lambda": "Lambda",
            "Elastic Compute Cloud": "EC2",
            "Amazon S3": "S3",
            "Elastic Block Store": "EBS",
            "Amazon RDS": "RDS",
            "Amazon DynamoDB": "DynamoDB",
            "Amazon Redshift": "Redshift",
            "Amazon VPC": "VPC",
            "Elastic Load Balancing": "ELB",
            "Amazon CloudFront": "CloudFront"
        }

    def get_node(self, node_type: str) -> Any:
        # Simulated retrieval of a node
        for category, components in self.components.items():
            if node_type in components:
                return f"Node of type {node_type} in category {category}"
        return None

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category:
            if category in self.components:
                return {category: self.components[category]}
            else:
                return {}
        return self.components
