
from diagrams.aws import *
from typing import List, Dict, Any


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        self.categories = self._discover_categories()
        self.components = self._discover_components()
        self.aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        categories = [name for name in dir(diagrams.aws) if name.isupper()]
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        components = {}
        for category in self.categories:
            module = getattr(diagrams.aws, category)
            component_names = [name for name in dir(
                module) if not name.startswith('__')]
            components[category] = component_names
        return components

    def _build_aliases(self) -> Dict[str, str]:
        aliases = {}
        for category, component_names in self.components.items():
            module = getattr(diagrams.aws, category)
            for component_name in component_names:
                component = getattr(module, component_name)
                aliases[component_name.lower()] = component
        return aliases

    def get_node(self, node_type: str) -> Any:
        return self.aliases.get(node_type.lower())

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category:
            category = category.upper()
            if category in self.components:
                return {category: self.components[category]}
            else:
                return {}
        else:
            return self.components
