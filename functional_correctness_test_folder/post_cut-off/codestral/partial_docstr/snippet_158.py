
from typing import List, Dict, Any
from diagrams import aws


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        self._categories = self._discover_categories()
        self._components = self._discover_components()
        self._aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        return [category for category in dir(aws) if not category.startswith('_')]

    def _discover_components(self) -> Dict[str, List[str]]:
        components = {}
        for category in self._categories:
            components[category] = [component for component in dir(
                getattr(aws, category)) if not component.startswith('_')]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        aliases = {}
        for category, components in self._components.items():
            for component in components:
                aliases[f"{category}.{component}"] = f"{category}.{component}"
                aliases[component.lower()] = f"{category}.{component}"
        return aliases

    def get_node(self, node_type: str) -> Any:
        if node_type not in self._aliases:
            raise ValueError(
                f"Node type '{node_type}' not found in AWS components.")
        category, component = self._aliases[node_type].split('.')
        return getattr(getattr(aws, category), component)

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category:
            if category not in self._components:
                raise ValueError(
                    f"Category '{category}' not found in AWS components.")
            return {category: self._components[category]}
        return self._components
