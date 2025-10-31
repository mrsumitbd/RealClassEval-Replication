
from typing import List, Dict, Any


class AWSComponentRegistry:

    def __init__(self):
        # Simulated AWS categories and components
        self._categories = [
            "Compute",
            "Storage",
            "Database",
            "Networking",
            "Machine Learning"
        ]
        self._components = {
            "Compute": ["EC2", "Lambda", "ECS", "EKS"],
            "Storage": ["S3", "EBS", "EFS", "Glacier"],
            "Database": ["RDS", "DynamoDB", "Redshift", "Aurora"],
            "Networking": ["VPC", "Route53", "CloudFront", "API Gateway"],
            "Machine Learning": ["SageMaker", "Comprehend", "Rekognition"]
        }
        self._aliases = self._build_aliases()
        self._node_definitions = {
            "EC2": {"type": "Compute", "desc": "Elastic Compute Cloud"},
            "Lambda": {"type": "Compute", "desc": "Serverless compute"},
            "ECS": {"type": "Compute", "desc": "Elastic Container Service"},
            "EKS": {"type": "Compute", "desc": "Elastic Kubernetes Service"},
            "S3": {"type": "Storage", "desc": "Simple Storage Service"},
            "EBS": {"type": "Storage", "desc": "Elastic Block Store"},
            "EFS": {"type": "Storage", "desc": "Elastic File System"},
            "Glacier": {"type": "Storage", "desc": "Archival storage"},
            "RDS": {"type": "Database", "desc": "Relational Database Service"},
            "DynamoDB": {"type": "Database", "desc": "NoSQL Database"},
            "Redshift": {"type": "Database", "desc": "Data Warehouse"},
            "Aurora": {"type": "Database", "desc": "MySQL/PostgreSQL-compatible DB"},
            "VPC": {"type": "Networking", "desc": "Virtual Private Cloud"},
            "Route53": {"type": "Networking", "desc": "DNS Service"},
            "CloudFront": {"type": "Networking", "desc": "Content Delivery Network"},
            "API Gateway": {"type": "Networking", "desc": "API Management"},
            "SageMaker": {"type": "Machine Learning", "desc": "ML Platform"},
            "Comprehend": {"type": "Machine Learning", "desc": "NLP Service"},
            "Rekognition": {"type": "Machine Learning", "desc": "Image/Video Analysis"}
        }

    def _discover_categories(self) -> List[str]:
        return list(self._categories)

    def _discover_components(self) -> Dict[str, List[str]]:
        return {cat: list(comps) for cat, comps in self._components.items()}

    def _build_aliases(self) -> Dict[str, str]:
        # Example aliases for some components
        aliases = {
            "Elastic Compute Cloud": "EC2",
            "Simple Storage Service": "S3",
            "Relational Database Service": "RDS",
            "Virtual Private Cloud": "VPC",
            "Content Delivery Network": "CloudFront",
            "API Management": "API Gateway",
            "ML Platform": "SageMaker"
        }
        # Add lower-case aliases for convenience
        for comp in sum(self._components.values(), []):
            aliases[comp.lower()] = comp
        return aliases

    def get_node(self, node_type: str) -> Any:
        # Try direct match
        if node_type in self._node_definitions:
            return self._node_definitions[node_type]
        # Try alias match
        if node_type in self._aliases:
            real_name = self._aliases[node_type]
            return self._node_definitions.get(real_name)
        # Try case-insensitive match
        node_type_lower = node_type.lower()
        if node_type_lower in self._aliases:
            real_name = self._aliases[node_type_lower]
            return self._node_definitions.get(real_name)
        return None

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category is None:
            return self._discover_components()
        # Try direct match
        if category in self._components:
            return {category: list(self._components[category])}
        # Try case-insensitive match
        for cat in self._components:
            if cat.lower() == category.lower():
                return {cat: list(self._components[cat])}
        return {}
